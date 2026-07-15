from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from core.models import SiteSettings
from editorials.models import Category, Post, Tag
from ads.models import Ad

IMG = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/"

POSTS = [
    {
        "title": "Dhaka, London to work together in communication sectors",
        "category": "Bangladesh",
        "tags": ["Diplomacy", "Transport"],
        "image": IMG + "AVvXsEjXFckK3U8shHrr3cOcxW4CJLrh5EB6T9BpmPw0kBrKNNG7vRqIUFrb70yMUzhvkz4gySrZNfXjTvjCYuUUwFJyRnjS1ceX-n75Yg0HfTGX6g5jw05G7gHeFn6v5FBnawp0pZWjUW-5K-jyng0e3B9ukU2LIfHv0UnWIMolU1SM8K_3GKAE3VoMnPKXQo1e/w72-h72-p-k-no-nu/1000589172.jpg",
        "date": "2026-07-10",
        "featured": True,
        "body": """<p>DHAKA, July 10, 2026 (BSS) &mdash; Dhaka and London have reaffirmed their commitment to working together to further strengthen existing cooperation in transport, shipping, railways, port development, trade, investment, and other areas of mutual interest.</p>
<p>The two sides reaffirmed it in a bilateral meeting between Bangladesh's Minister for Road Transport and Bridges, Shipping and Railways and the United Kingdom's Secretary of State for Transport yesterday in London, said an official handout here today.</p>
<p>Bangladesh's minister conveyed the greetings of the Prime Minister to the UK Transport Secretary. He said Bangladesh's current government assumed office through a free, fair, inclusive, and peaceful election with the overwhelming support of the people and remains firmly committed to strengthening democracy, good governance, accountability, and the rule of law.</p>
<p>Referring to the longstanding historical, friendly, and multifaceted relations between Bangladesh and the United Kingdom, the minister expressed appreciation for the UK's support for Bangladesh's development journey.</p>""",
    },
    {
        "title": "Egypt reach first-ever World Cup knockout stage after 1-1 draw against Iran",
        "category": "Sports",
        "tags": ["Football", "World Cup"],
        "image": IMG + "AVvXsE86BzdIEUP3wrWHyIyjXq3APntwFWMuBQSIWjJi6Hrin2LYMqjiIwGROtPcuIXoGXulL7OJNehG2B_uAKwgJib553MZm4ejolPWMy2uq387RmBxigY0jKXLaKYVZbRYeuLfHOSl10iaIJT4HunuTd3DK0KylKf873Lcd8c9dpXwtCRpVdOHo_sAKKqi5-s/w72-h72-p-k-no-nu/1000585522.jpg",
        "date": "2026-06-27",
        "featured": True,
        "body": """<p>CAIRO, June 27, 2026 (NT) &mdash; Egypt secured a historic place in the FIFA World Cup knockout stage for the first time ever after a hard-fought 1-1 draw against Iran in their final group match.</p>
<p>A late equaliser from the penalty spot ensured the Pharaohs finished among the best third-placed sides and booked a last-16 berth that had eluded them in every previous appearance.</p>
<p>Coach and players dedicated the milestone to the nation, promising an even stronger showing in the knockouts as millions celebrated across the country.</p>""",
    },
    {
        "title": "Security beefed up to avert chaos over AL founding anniv",
        "category": "Politics",
        "tags": ["Security", "Dhaka"],
        "image": IMG + "AVvXsEiUPhtm61qQv6MmDpKFrvI2NyXbwShpamDFwYoCGz4BV3HDwetnMN1WX0l0TygrowCs6BAvNzExMM8FGC4V2dIr8A9KF9alOPhRDvln0vXpdHVo4VeETly4jVKOte26nHrOEh2luBCzHp2B9UpWLyy8FImYs_3g2WL7ABxki31f2ra3lLvclPs01pq9FKDB/w72-h72-p-k-no-nu/1000584368.jpg",
        "date": "2026-06-23",
        "featured": True,
        "body": """<p>DHAKA, June 23, 2026 (NT) &mdash; Law enforcers have stepped up security across the capital to prevent any untoward incident ahead of the founding anniversary programmes.</p>
<p>Additional police and rapid-action detachments have been deployed at key points, with traffic diversions planned around venues hosting large gatherings.</p>
<p>Authorities urged citizens to cooperate with security personnel and report any suspicious activity immediately.</p>""",
    },
    {
        "title": "Iran Guards say targeted US base in Jordan with missiles",
        "category": "World",
        "tags": ["Middle East", "Conflict"],
        "image": IMG + "AVvXsEhMfPrKX1YwdI480SlYnNCIhNVPcwqyjPrkK23RrVkImi4dbaWKIcXFnKpbs4PkFsMX6XXr9lGKy6eQEVcdbf0T_BJOljpQCj7g6zorTRatZk66KEbgrMk3tXYgpAR525MWVu6j76bV5qCS-mw03IVy3DzYjo3ZJYqkSN6s3lRn0CAz4hjeD3EBVs0KOFpH/w72-h72-p-k-no-nu/1000581076.jpg",
        "date": "2026-06-10",
        "featured": True,
        "body": """<p>TEHRAN, June 10, 2026 (NT) &mdash; Iran's Revolutionary Guards said they targeted a US military base in Jordan with missiles in response to recent strikes, raising fears of a wider regional escalation.</p>
<p>The Pentagon confirmed the incident and said it was assessing the damage. Washington urged restraint while reaffirming its commitment to defend its forces in the region.</p>
<p>Diplomats stepped up contacts to de-escalate as oil prices spiked on the news.</p>""",
    },
    {
        "title": "Mosaddek, Nahid star as Tigers end 21-year ODI wait against Aussies with thumping win",
        "category": "Sports",
        "tags": ["Cricket", "Bangladesh"],
        "image": IMG + "AVvXsEhCrSWtqJnTSGLAHEfscag2i1IU0Vx1zDQphdIYFRWwSFrg8hdv0eaFoLSimjKKb-HFCechldGDmS0mxj5JVkxZM_hmR-n12rhsLpNsLq-fuZ-KNqq4qfgIlCUVObVG7uUGrBwF30YPkCYIlRW97a3Vzh_GDEyGTHL4Dy6qI1Nct1Y_1i-y5lgtXG85xd2z/w72-h72-p-k-no-nu/1000581075.webp",
        "date": "2026-06-10",
        "body": """<p>DHAKA, June 10, 2026 (NT) &mdash; Mosaddek Hossain and Nahid Rana produced match-winning performances as Bangladesh ended a 21-year wait for an ODI victory over Australia with a commanding win at home.</p>
<p>Chasing a testing total, Mosaddek's composed half-century anchored the innings while Nahid's fiery spell earlier ripped through the top order.</p>
<p>Captain praised the youngsters, saying the result marks a new era for Bangladeshi cricket.</p>""",
    },
    {
        "title": "Hannan Masud in Parliament: Gen Z doesn't want 1972 constitution",
        "category": "Politics",
        "tags": ["Constitution", "Parliament"],
        "image": IMG + "AVvXsEhMfPrKX1YwdI480SlYnNCIhNVPcwqyjPrkK23RrVkImi4dbaWKIcXFnKpbs4PkFsMX6XXr9lGKy6eQEVcdbf0T_BJOljpQCj7g6zorTRatZk66KEbgrMk3tXYgpAR525MWVu6j76bV5qCS-mw03IVy3DzYjo3ZJYqkSN6s3lRn0CAz4hjeD3EBVs0KOFpH/w72-h72-p-k-no-nu/1000581076.jpg",
        "date": "2026-03-30",
        "body": """<p>DHAKA, March 30, 2026 (NT) &mdash; Hannan Masud told Parliament that Generation Z does not want the 1972 constitution in its current form, calling for a national conversation on reform.</p>
<p>The remarks triggered heated debate, with ruling and opposition lawmakers exchanging barbs over the roadmap for any constitutional change.</p>
<p>Constitutional experts said any amendment would require broad consensus and a clear public mandate.</p>""",
    },
    {
        "title": "Plan to Complete SSC and HSC Exams by December 31",
        "category": "Education",
        "tags": ["Exams", "Education"],
        "image": IMG + "AVvXsEi1x_wVL323uPi3LilxY1VDMBCbnnH_8VsAOaa9u-A9T7Sy3nxYg25n_ZI_FrMjDxWsVOZFd6QRJoGNO5EsFPSPWYtjy873sUSRbXGyr0PZp_7l88H5az2sMY8XMgsGRIt2_qAtV7sauv-xwzeSv7y6Xv9pOtcnOAva0-rXu09dqWvCwKTHdsSM5jLnF6kx/w72-h72-p-k-no-nu/657356511_2199837217492864_8598807639487180316_n_1.webp",
        "date": "2026-03-25",
        "body": """<p>DHAKA, March 25, 2026 (NT) &mdash; The education authorities have drawn up a plan to complete both SSC and HSC examinations by December 31, aiming to bring the academic calendar back on track.</p>
<p>Officials said extended routines and additional centres would be used to clear the backlog caused by earlier disruptions.</p>
<p>Students and parents welcomed the clarity, though some raised concerns about preparation time.</p>""",
    },
    {
        "title": "Dhaka ranks 4th globally in air pollution with unhealthy AQI",
        "category": "Bangladesh",
        "tags": ["Environment", "Health"],
        "image": IMG + "AVvXsEhnErzYhlJK3001pKF0CRVjV-1rDI6RK3_ycHzQvpwYesYdKaXKsDEJPParGH_q1cz9XpDAdcCmwISrXx41yGo_wCcbB-1YWx8loZeTe4j30uc-42DF080vI3sji6y57_Fwqqb3eBGpyghZP562HuMZZNwnLnIL2h8AVoQEnIpwDV-s_Cp8Ol6RUI9ZjL2J/w72-h72-p-k-no-nu/b98f1c7b50f513a56396fd3e9d93a659-6926a1a8ac6bf.webp",
        "date": "2026-03-24",
        "body": """<p>DHAKA, March 24, 2026 (NT) &mdash; Dhaka ranked fourth worst in the world for air quality as its Air Quality Index slipped into the unhealthy category early Tuesday.</p>
<p>Environmentalists blamed vehicular emissions, construction dust and crop burning in adjoining regions for the seasonal spike.</p>
<p>They advised vulnerable groups to limit outdoor activity and urged stricter enforcement of emission norms.</p>""",
    },
    {
        "title": "Trump says Iran 'wants to make a deal' but Tehran denies talks as deadline extended",
        "category": "World",
        "tags": ["US", "Diplomacy"],
        "image": IMG + "AVvXsEjZjnoA1fslaB796wTiQaGxj-LK10ydym9cSfFFIqNq9OHFNWV_v_jQ8EZtDD6S6ulE3b2QGWBrWD_CnEfFBzC-VKHzdJldI183fPS5X7u5zH00riYytTA8yEC0aZbpSlGoIEyUOou-Pa0nf9zbTFYy9Wu8S3D7hN0orqgEx8rcyz9phQB3H2cSZpPp74cz/w72-h72-p-k-no-nu/6193197.webp",
        "date": "2026-03-24",
        "body": """<p>WASHINGTON, March 24, 2026 (NT) &mdash; Former US President Donald Trump said Iran "wants to make a deal", but Tehran denied any talks were underway as a negotiated deadline was extended.</p>
<p>The conflicting signals underscored the fragility of back-channel diplomacy aimed at curbing the stand-off.</p>
<p>Analysts said the extension lowers the risk of immediate confrontation but leaves the core disputes unresolved.</p>""",
    },
    {
        "title": "Dhaka's footpaths must be cleared by March to ease traffic, says DMP",
        "category": "Politics",
        "tags": ["Dhaka", "Traffic"],
        "image": IMG + "AVvXsEgmjncyGVIGioBjVkU8O1SxzZRXokV0byaDsI6vEnraGK5zdrBAE7NgCWJ3EG5p3g-MWtQSLNps1fKBgx-rqc-VZU0EEybJcSrTZq7dMV0K1xf3z3xYJDNSuQnQACeDOkhiDIiRhohwut1x0i9Z8eAlji4w2Z1G4KwO8dQzQq8RVOlCI3lBEuDOBWG2EwSX/w72-h72-p-k-no-nu/footpath-occupied-hotel-shop-080725-004-1751903128.jpg",
        "date": "2026-03-23",
        "body": """<p>DHAKA, March 23, 2026 (NT) &mdash; The Dhaka Metropolitan Police said footpaths across the city must be cleared by March to ease worsening traffic congestion.</p>
<p>Shop owners and vendors occupying walkways have been asked to comply voluntarily before a stricter drive begins.</p>
<p>DMP said dedicated teams will monitor key corridors to keep pedestrian paths free.</p>""",
    },
    {
        "title": "Govt plans modernisation of railway level crossings to prevent accidents",
        "category": "Bangladesh",
        "tags": ["Railway", "Safety"],
        "image": IMG + "AVvXsEiQ5FlGhrmM3V9d_FeC57GTH7IIHCY_fIWcfDnePldwG21ukUWvq4CmSLMryBBQQ_AzTaTuH6_QEOvKvivPsf1EJ6XwFZwsT3vInndgSDtEYAfbAPq4fbNdrlnbb2C8vkSnvRGhFHLQYUfWbyQIEIdeAFCq6GrvKX45QnrLmOhszFAHTJMJiseSi330VoYT/w72-h72-p-k-no-nu/ob_1774182574.jpg",
        "date": "2026-03-23",
        "body": """<p>DHAKA, March 23, 2026 (NT) &mdash; The government plans to modernise railway level crossings to prevent frequent accidents, the railways ministry said.</p>
<p>The programme includes automated gates, warning systems and the gradual conversion of busy crossings into overpasses.</p>
<p>Officials said public cooperation remains vital during the transition period.</p>""",
    },
    {
        "title": "Petrol pumps may shut down nationwide over fuel shortage, security risks, owners warn",
        "category": "Politics",
        "tags": ["Fuel", "Economy"],
        "image": IMG + "AVvXsEijFZIUsvnn2U_5K_K_h_h4QTh71I1q_8qoqIfvKda4ZcCOmFdels55htmI0OBDSchLsnp3UFAPLr49HoY2T9kBVUhN6doJ9CywV9i_ZKlU8jrxYMo8IdMN7ICQcke04P4Uh2Rl-KWRLPc1wlPhGPUy6YeuGe5qcKzoeb-g4nTSsyRrSy-jfyow5ANTx6r7/w72-h72-p-k-no-nu/de5bd3f20a2e8223fde35d3923c598a6-69aaa519d2f61.webp",
        "date": "2026-03-23",
        "body": """<p>DHAKA, March 23, 2026 (NT) &mdash; Petrol pump owners have warned they may shut down nationwide over a fuel shortage and rising security risks at outlets.</p>
<p>They demanded an urgent supply of fuel and better security arrangements to keep stations running.</p>
<p>The energy division assured that imports were being expedited to normalise the situation.</p>""",
    },
    {
        "title": "Driving mishaps during Eid: 400 alone get treatment at Nitor",
        "category": "Politics",
        "tags": ["Road Safety", "Health"],
        "image": IMG + "AVvXsEjDmfFAbbwLSLM5-pd05V0lzORa1JxW33Wbu5pgg2TyYEvHyxAWMeo17kJn7-kS7vjlrX518EiWtfck2q1LoAXTciq2rwX8_C6kTzgH1csq7z32US_yxDqOB8LDr0w8kWH_DW_9dlfw0ZSTxiAeNVO9BIKd-HQKq5wcY_f587vzZCuWRRa6KkcRc4m6n-U7/w72-h72-p-k-no-nu/757ce47031384d5dff0f2151bb108ff1-69bfdc1a974f8.webp",
        "date": "2026-03-23",
        "body": """<p>DHAKA, March 23, 2026 (NT) &mdash; More than 400 people injured in road mishaps during Eid celebrations alone received treatment at the National Institute of Traumatology and Orthopaedic Rehabilitation (Nitor).</p>
<p>Doctors said most cases involved motorcycles and reckless overtaking on packed highways.</p>
<p>They urged stricter traffic discipline during festive travel.</p>""",
    },
]


class Command(BaseCommand):
    help = "Seed sample categories, posts, ads and roles for the DNT site."

    def handle(self, *args, **options):
        # Site settings
        SiteSettings.get_settings()
        self.stdout.write("Site settings ready.")

        # Categories
        cat_map = {}
        for name in ["World", "Politics", "Bangladesh", "Education", "Sports"]:
            cat, _ = Category.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            if not cat.slug:
                cat.slug = slugify(name)
                cat.save()
            cat_map[name] = cat
        self.stdout.write(f"Categories: {len(cat_map)}")

        # Tags
        tag_map = {}
        for tname in ["Diplomacy", "Transport", "Football", "World Cup", "Security",
                      "Dhaka", "Conflict", "Middle East", "Cricket", "Bangladesh",
                      "Constitution", "Parliament", "Exams", "Education", "Environment",
                      "Health", "US", "Diplomacy", "Traffic", "Railway", "Safety",
                      "Fuel", "Economy", "Road Safety"]:
            tag, _ = Tag.objects.get_or_create(name=tname, defaults={"slug": slugify(tname)})
            if not tag.slug:
                tag.slug = slugify(tname)
                tag.save()
            tag_map[tname] = tag
        self.stdout.write(f"Tags: {len(tag_map)}")

        # Posts
        from django.contrib.auth.models import User

        authors = list(
            User.objects.filter(username__in=["admin", "editor1", "sub1", "reporter1"])
        )
        if not authors:
            authors = [None]
        created = 0
        for data in POSTS:
            if Post.objects.filter(title=data["title"]).exists():
                continue
            post = Post.objects.create(
                title=data["title"],
                category=cat_map[data["category"]],
                author=authors[created % len(authors)],
                author_name="National Times",
                excerpt=data["body"][:160].replace("<p>", "").replace("</p>", " ").strip(),
                content=data["body"],
                featured_image=data["image"],
                status="published",
                is_featured=data.get("featured", False),
                published_at=timezone.make_aware(
                    timezone.datetime.strptime(data["date"], "%Y-%m-%d")
                ),
            )
            for t in data.get("tags", []):
                if t in tag_map:
                    post.tags.add(tag_map[t])
            # give some posts view counts for "most viewed"
            post.views = 50 + created * 7
            post.save(update_fields=["views"])
            created += 1
        # Idempotent: backfill authors on posts seeded in earlier runs.
        for i, p in enumerate(Post.objects.filter(author=None)):
            p.author = authors[i % len(authors)]
            p.save(update_fields=["author"])
        self.stdout.write(f"Posts created: {created}")

        # Ads
        ad_specs = [
            ("Home Top Banner", Ad.SLOT_HOME_TOP, "https://nagadwcquiz.com/assets/FIFA-World-Cup-Quiz-Campaign_970X250.gif", "https://nagadwcquiz.com/"),
            ("Sidebar Ad 1", Ad.SLOT_SIDEBAR, "https://files.dainikshiksha.com/181414/21-June-2026.gif", "https://dainikshiksha.com/"),
            ("Article Bottom", Ad.SLOT_ARTICLE_BOTTOM, "https://s13.gifyu.com/images/b7ESk.gif", "https://gifyu.com/"),
        ]
        for name, slot, image, link in ad_specs:
            Ad.objects.get_or_create(name=name, slot=slot, defaults={"image_url": image, "link": link})
        self.stdout.write("Ads ready.")

        # Roles + demo users
        User = get_user_model()
        for username, role in [("editor1", "Editor"), ("sub1", "SubEditor"), ("reporter1", "Reporter")]:
            user, made = User.objects.get_or_create(username=username, defaults={"email": f"{username}@dnt.bd"})
            if made:
                user.set_password("editor12345")
                user.save()
            group = Group.objects.get(name=role)
            user.groups.add(group)
        admin, made = User.objects.get_or_create(username="admin", defaults={"email": "admin@dnt.bd", "is_staff": True, "is_superuser": True})
        if made:
            admin.set_password("admin12345")
            admin.save()
        self.stdout.write("Roles and demo users ready (admin/admin12345, editor1/sub1/reporter1 : editor12345).")
        self.stdout.write(self.style.SUCCESS("Seed complete."))
