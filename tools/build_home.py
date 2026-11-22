"""Builds content/home.html (the Welcome page) as native WordPress blocks.
Content and image URLs come from the live Elementor page 359 (read only export, Nov 22, 2026).
Run: python3 -I tools/build_home.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ncah_blocks import *

out = []

# 1. Hero slider (4 slides, as on the live site)
hero = ('<!-- wp:group {"align":"full","className":"ncah-hero","layout":{"type":"default"}} -->\n<div class="wp-block-group alignfull ncah-hero">'
        + '\n\n'.join([
            slide(U + '2026/10/IMG_3257-scaled.webp', '', 'Get Your Tickets', 'https://www.zeffy.com/en-CA/ticketing/annual-gala-8173', red=True),
            slide(U + '2026/10/DSC_6472-scaled.webp', 'Connect | Engage | Empower', 'Learn More', '/about-us/'),
            slide(U + '2026/10/DSC_6368-scaled.webp', 'Celebrating Nigeria @ 66', 'View Our Events', '/events/'),
            slide(U + '2026/10/DSC_7787.webp', 'Golden Eagles, Winners 2026 Hamilton AFCON', 'Discover Golden Eagles', 'https://soccer.ncahamilton.ca/'),
        ]) + '</div>\n<!-- /wp:group -->')
out.append(hero)

# 2. Welcome: Green Spirit Initiative intro and video
gsi = card(U + '2024/04/Photo-Background.webp', 'Introducing The Green Spirit Initiative (GSI)',
           'The Green Spirit Initiative (GSI) is the charitable arm of the NCAH, dedicated to empowering visible minorities and newcomers through community-focused support. Inspired by the Nigerian flag, the initiative focuses on improving social determinants of health to build a more inclusive and prosperous society.')
vid = youtube('https://youtu.be/sX1wZYc0SRE', '25th Annual Community BBQ')
out.append(band(columns([column(gsi, '65%'), column(vid, '35%')]), 'mist', 'ncah-welcome'))

# 3. Event Gallery: latest posts (replaces the Elementor events loop carousel)
q = ('<!-- wp:query {"query":{"perPage":8,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","inherit":false},"className":"ncah-events"} -->\n'
     '<div class="wp-block-query ncah-events"><!-- wp:post-template {"layout":{"type":"grid","columnCount":4}} -->\n'
     '<!-- wp:post-featured-image {"isLink":true,"aspectRatio":"4/3"} /-->\n\n'
     '<!-- wp:post-date {"fontSize":"small"} /-->\n\n'
     '<!-- wp:post-title {"level":3,"isLink":true,"fontSize":"medium"} /-->\n'
     '<!-- /wp:post-template --></div>\n<!-- /wp:query -->')
out.append(band(heading('Event Gallery', 2, '', 'center', 'x-large', 'ncah-green') + '\n\n' + q + '\n\n' +
                buttons([button('View all events', '/events/')]), 'mist', 'ncah-events-band', '1250px'))

# 4. Event videos (the Elementor video playlist, as an embed grid)
vids = [('25th Annual Community BBQ', 'https://youtu.be/sX1wZYc0SRE'),
        ('Recap of the 2024 End of Year Multicultural Gala', 'https://youtu.be/2C_wG8mLvjU'),
        ('Recap of the 2023 End of Year Gala', 'https://youtu.be/re8Eo57vFz4'),
        ('Games at the 2023 NCAH End of the Year Gala Nite', 'https://youtu.be/kRSui43Jt0Y'),
        ("2023 End of the Year Party, President's Speech", 'https://youtu.be/MoHHh-VlVIk'),
        ('Inauguration of the 2023 to 2025 Executive Members', 'https://youtu.be/wIr1ipqrP1g'),
        ('NCAHamilton 2023 Summer Picnic', 'https://youtu.be/OnTW_Swx1r0')]
grid = ('<!-- wp:group {"layout":{"type":"grid","columnCount":3}} -->\n<div class="wp-block-group">'
        + '\n\n'.join(youtube(u, t) for t, u in vids) + '</div>\n<!-- /wp:group -->')
out.append(band(heading('Videos', 2, '', 'center', 'x-large', 'ncah-green') + '\n\n' + grid, None, 'ncah-videos'))

# 5. Community, Mission, Goals
three = columns([
    column(card(U + '2023/12/About-the-Association.webp', 'Community', 'The Nigerian Canadian Association, Hamilton (NCAH) was established in February 1999 as a non-profit, non-political association with the aim of fostering a supportive environment for Nigerians in Hamilton.')),
    column(card(U + '2023/12/The-Nigerian-Spirit-1.webp', 'Our Mission', 'Our mission is to promote unity and provide a conducive environment for individuals with Nigerian heritage to thrive in the community.')),
    column(card(U + '2023/12/binds-us-1.webp', 'Our Goals', 'Our goals include promoting Nigerian culture, encouraging multicultural dialogues, providing cultural identity, helping members in need, and serving as a social and economic network for members and the broader community.')),
])
out.append(band(three, 'mist', 'ncah-who'))

# 6. Membership and benefits
benefits = [('Networking Opportunities', 'Access to a network of professionals and community members for personal and professional growth.'),
            ('Engagement', 'Participate in events, discussions, and activities promoting Nigerian culture and heritage.'),
            ('Educational Resources', 'Access to workshops, virtual clinics, and resources aimed at personal and professional development.'),
            ('Member Support', 'Receive support during challenging times, and contribute to the support of others within the community.'),
            ('Information Sharing', 'Stay informed on community news, events, and other relevant updates through regular meetings and communications.'),
            ('Leadership Development', 'Opportunities to take on leadership roles within the community, contributing to its growth and direction.'),
            ('Discounts', 'Enjoy discounts on event tickets, hall rentals, and selected community businesses.'),
            ('Representation', 'Have a voice in community matters and contribute to the collective decisions impacting the association.')]
bgrid = ('<!-- wp:group {"layout":{"type":"grid","columnCount":4}} -->\n<div class="wp-block-group">' +
         '\n\n'.join('<!-- wp:group {"className":"ncah-benefit","layout":{"type":"default"}} -->\n<div class="wp-block-group ncah-benefit">'
                     + heading(t, 3, '', None, 'medium', 'ncah-green') + '\n\n' + para(d, size='small') + '</div>\n<!-- /wp:group -->' for t, d in benefits)
         + '</div>\n<!-- /wp:group -->')
mem = card(U + '2023/12/settlement.webp', 'Membership', "Membership in the Nigerian Canadian Association, Hamilton, offers a pathway to enriching experiences, meaningful relationships, and a sense of belonging in a community that values each member's contribution.")
out.append(band(columns([column(mem, '35%'), column(bgrid, '65%')]) + '\n\n' + buttons([button('Become a member', '/membership/', True)]), 'mist', 'ncah-membership'))

# 7. Partners
partners = [('2025/12/ACCA.webp', 'ACCA'), ('2025/12/Davisol.webp', 'Davisol'), ('2025/12/Hamilton-Urban-Core.webp', 'Hamilton Urban Core'),
            ('2025/12/HBHCLF.webp', 'Hamilton Black Health Community Leaders Forum'), ('2025/12/Isreal-Iyamu.webp', 'Israel Iyamu'),
            ('2025/12/Refune-Newcomer-Health.webp', 'Refuge Newcomer Health'), ('2025/07/CEFund-and-Hamilton-logo-black.webp', 'City Enrichment Fund, City of Hamilton')]
logos = ('<!-- wp:group {"className":"ncah-logos","layout":{"type":"flex","flexWrap":"wrap","justifyContent":"center","verticalAlignment":"center"}} -->\n<div class="wp-block-group ncah-logos">'
         + '\n\n'.join(logo(U + p, a) for p, a in partners) + '</div>\n<!-- /wp:group -->')
out.append(band(heading('Our Partners', 2, '', 'center', 'x-large', 'ncah-green') + '\n\n' +
                para('We would like to extend our heartfelt gratitude to the following organizations and individuals for their generous support. Your contributions have made a significant impact on our community and enabled us to continue promoting Nigerian culture and heritage in Canada.', align='center') + '\n\n' + logos, 'mist', 'ncah-partners'))

p = pathlib.Path(__file__).resolve().parent.parent / 'content' / 'home.html'
p.write_text('\n\n'.join(out) + '\n')
print('wrote', p, len('\n\n'.join(out)), 'bytes')
