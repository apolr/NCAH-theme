"""Builds content/home.html (the Welcome page), redesigned in the layout and simplicity of ncabc.org.
Text and image URLs come from the live ncahamilton.ca Welcome page (read only, Nov 22, 2026).
Run: python3 -I tools/build_home.py
"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ncah_blocks import *

def cover(img, inner, cls, dim=45, minh=340, pos=None):
    a = {'url': img, 'dimRatio': dim, 'isDark': True, 'minHeight': minh, 'className': cls}
    if pos: a['contentPosition'] = pos
    return (f'<!-- wp:cover {json.dumps(a, separators=(",", ":"))} -->\n<div class="wp-block-cover is-dark {cls}" style="min-height:{minh}px">'
            f'<span aria-hidden="true" class="wp-block-cover__background has-background-dim-{dim} has-background-dim"></span>'
            f'<img class="wp-block-cover__image-background" alt="" src="{img}" data-object-fit="cover"/>'
            f'<div class="wp-block-cover__inner-container">{inner}</div></div>\n<!-- /wp:cover -->')

def eyebrow(t, color=None):
    return heading(t, 3, 'ncah-eyebrow', None, None, color)

out = []

# 1. Hero: one full bleed photo, big serif title, short line, two buttons
hero_inner = (heading('Nigerian Canadian Association, Hamilton and Environs', 1, '', 'center', 'hero', 'white') + '\n\n' +
              para('Celebrating Heritage. Fostering Interactions. Providing Support.', align='center', color='white') + '\n\n' +
              buttons([button('Learn more', '/about-us/', True), button('Get your gala tickets', 'https://www.zeffy.com/en-CA/ticketing/annual-gala-8173')]))
out.append(cover(U + '2026/10/DSC_6472-scaled.webp', hero_inner, 'ncah-hero1 alignfull', 50, 720, 'center center').replace('wp-block-cover is-dark', 'wp-block-cover alignfull is-dark', 1))

# 2. Get involved: four photo tiles
def tile(img, title, text, url):
    inner = heading(title, 3, '', None, None, 'white') + '\n\n' + para(text, size='small', color='white')
    return column(f'<a href="{url}" class="ncah-tile-link">' + cover(img, inner, 'ncah-tile', 35, 340, 'bottom left') + '</a>')
tiles = columns([
    tile(U + '2023/12/About-the-Association.webp', 'About us', 'Who we are and how we serve our community.', '/about-us/'),
    tile(U + '2023/12/settlement.webp', 'Membership', 'Join the Association and belong.', '/membership/'),
    tile(U + '2026/10/DSC_7787.webp', 'Programs', 'Youth, sports and community programs.', '/programs/'),
    tile(U + '2023/12/The-Nigerian-Spirit-1.webp', 'Donate', 'Support our work with a gift.', '/donate/'),
], 'ncah-tiles')
out.append(band(heading('Start your journey', 2, '', 'center', 'x-large') + '\n\n' +
                para('The Nigerian Canadian Association, Hamilton (NCAH) was established in February 1999 as a non-profit, non-political association with the aim of fostering a supportive environment for Nigerians in Hamilton.', align='center'), None, 'ncah-journey', '820px'))
out.append('<!-- wp:group {"align":"full","layout":{"type":"default"}} -->\n<div class="wp-block-group alignfull">' + tiles + '</div>\n<!-- /wp:group -->')

# 3. Membership: green band, text left, button right, four cards
benefits = [('Networking Opportunities', 'Access to a network of professionals and community members for personal and professional growth.'),
            ('Engagement', 'Participate in events, discussions, and activities promoting Nigerian culture and heritage.'),
            ('Educational Resources', 'Access to workshops, virtual clinics, and resources aimed at personal and professional development.'),
            ('Member Support', 'Receive support during challenging times, and contribute to the support of others within the community.'),
            ('Information Sharing', 'Stay informed on community news, events, and other relevant updates through regular meetings and communications.'),
            ('Leadership Development', 'Opportunities to take on leadership roles within the community, contributing to its growth and direction.'),
            ('Discounts', 'Enjoy discounts on event tickets, hall rentals, and selected community businesses.'),
            ('Representation', 'Have a voice in community matters and contribute to the collective decisions impacting the association.')]

cards = [(U + '2023/12/binds-us-1.webp',) , (U + '2023/12/About-the-Association.webp',), (U + '2023/12/hi-res-be6cc83762096029bbf781b08a079cb8_crop_north-scaled.webp',), (U + '2023/07/IMG-20230730-WA0012.webp',)]
def mcard(img, t, d):
    return column('<!-- wp:group {"className":"ncah-mcard","layout":{"type":"default"}} -->\n<div class="wp-block-group ncah-mcard">'
                  f'<!-- wp:image {{"sizeSlug":"large","linkDestination":"none"}} -->\n<figure class="wp-block-image size-large"><img src="{img}" alt=""/></figure>\n<!-- /wp:image -->\n\n'
                  '<!-- wp:group {"className":"ncah-mbody","layout":{"type":"default"}} -->\n<div class="wp-block-group ncah-mbody">' + eyebrow(t) + '\n\n' + para(d) + '</div>\n<!-- /wp:group --></div>\n<!-- /wp:group -->')
cards += [(U + '2023/12/settlement.webp',), (U + '2023/12/The-Nigerian-Spirit-1.webp',), (U + '2026/10/DSC_6472-scaled.webp',), (U + '2026/10/DSC_6368-scaled.webp',)]
four = columns([mcard(cards[i][0], benefits[i][0], benefits[i][1]) for i in range(4)]) + '\n\n' + columns([mcard(cards[i][0], benefits[i][0], benefits[i][1]) for i in range(4, 8)])
memtext = ('Membership is voluntary and open to all peoples of Nigeria by birth, naturalization, marriage or heritage, and to others committed to the principles of the Association.')
mem = (columns([column(heading('NCAH Membership', 2, '', None, 'x-large', 'white') + '\n\n' + para(memtext, color='white'), '70%'),
                column(buttons([button('Become a member', '/membership/', True)], center=False), '30%')]) + '\n\n' + four)
out.append(band(mem, None, 'ncah-green-band ncah-membership'))

# 4. Upcoming event: the Gala
gala_text = (eyebrow('Saturday, December 5, 2026, 5 PM') + '\n\n' + heading('2026 NCAH Annual Gala: 5v5!', 3, '', None, None) + '\n\n' +
             para('Grand Olympia, Stoney Creek') + '\n\n' + buttons([button('Get your tickets', 'https://www.zeffy.com/en-CA/ticketing/annual-gala-8173', True)], center=False))
gala = ('<!-- wp:group {"className":"ncah-event-card","layout":{"type":"default"}} -->\n<div class="wp-block-group ncah-event-card">' +
        columns([column(f'<!-- wp:image {{"sizeSlug":"large","linkDestination":"none"}} -->\n<figure class="wp-block-image size-large"><img src="{U}2026/10/IMG_3257-scaled.webp" alt="2026 NCAH Annual Gala"/></figure>\n<!-- /wp:image -->', '45%'),
                 column('<!-- wp:group {"style":{"spacing":{"padding":{"top":"2.5rem","bottom":"2.5rem","left":"2.5rem","right":"2.5rem"}}},"layout":{"type":"default"}} -->\n<div class="wp-block-group" style="padding:2.5rem">' + gala_text + '</div>\n<!-- /wp:group -->', '55%')]) +
        '</div>\n<!-- /wp:group -->')
out.append(band(heading('Upcoming events', 2, '', 'center', 'x-large') + '\n\n' + gala, None, 'ncah-upcoming', '1100px'))

# 5. Green Spirit Initiative and video
gsi = (eyebrow('Green Spirit Initiative') + '\n\n' + heading('The charitable arm of the NCAH', 2, '', None, 'x-large') + '\n\n' +
       para('The Green Spirit Initiative (GSI) is the charitable arm of the NCAH, dedicated to empowering visible minorities and newcomers through community-focused support. Inspired by the Nigerian flag, the initiative focuses on improving social determinants of health to build a more inclusive and prosperous society.'))
out.append(band(columns([column(gsi, '55%'), column(youtube('https://youtu.be/sX1wZYc0SRE', '25th Annual Community BBQ'), '45%')]), 'mist', 'ncah-gsi'))

# 5b. Golden Eagles
ge = (eyebrow('Youth and Sports Directorate', 'ncah-red') + '\n\n' + heading('Golden Eagles, Winners 2026 Hamilton AFCON', 2, '', None, 'x-large') + '\n\n' +
      para('Our community soccer team plays under the Youth and Sports Directorate. Visit the Golden Eagles site for news, fixtures and the squad.') + '\n\n' +
      buttons([button('Discover Golden Eagles', 'https://soccer.ncahamilton.ca/', True)], center=False))
geimg = f'<!-- wp:image {{"sizeSlug":"large","className":"ncah-split-img"}} -->\n<figure class="wp-block-image size-large ncah-split-img"><img src="{U}2026/10/DSC_7787.webp" alt="Golden Eagles of Hamilton"/></figure>\n<!-- /wp:image -->'
out.append(band(columns([column(geimg, '50%'), column(ge, '50%')], 'ncah-split'), None, 'ncah-golden'))

# 6. News: latest posts
q = ('<!-- wp:query {"query":{"perPage":6,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","inherit":false},"className":"ncah-events"} -->\n'
     '<div class="wp-block-query ncah-events"><!-- wp:post-template {"layout":{"type":"grid","columnCount":3}} -->\n'
     '<!-- wp:post-featured-image {"isLink":true,"aspectRatio":"4/3"} /-->\n\n<!-- wp:post-date /-->\n\n'
     '<!-- wp:post-title {"level":3,"isLink":true,"fontSize":"large"} /-->\n<!-- /wp:post-template --></div>\n<!-- /wp:query -->')
out.append(band(heading('NCAH news and events', 2, '', 'center', 'x-large') + '\n\n' + q + '\n\n' + buttons([button('View all events', '/events/', True)]), None, 'ncah-news'))

# 7. Videos (first three; the rest can live on a Gallery page later)
from build_home_vids import VIDS as vids

grid = ('<!-- wp:group {"layout":{"type":"grid","columnCount":3}} -->\n<div class="wp-block-group">'
        + '\n\n'.join(youtube(u, t) for t, u in vids[:3]) + '</div>\n<!-- /wp:group -->')
out.append(band(heading('Watch', 2, '', 'center', 'x-large') + '\n\n' + grid + '\n\n' + buttons([button('More videos', '/gallery/', True)]), 'mist', 'ncah-videos'))

# 8. Partners
partners = [('2025/12/ACCA.webp', 'ACCA'), ('2025/12/Davisol.webp', 'Davisol'), ('2025/12/Hamilton-Urban-Core.webp', 'Hamilton Urban Core'),
            ('2025/12/HBHCLF.webp', 'Hamilton Black Health Community Leaders Forum'), ('2025/12/Isreal-Iyamu.webp', 'Israel Iyamu'),
            ('2025/12/Refune-Newcomer-Health.webp', 'Refuge Newcomer Health'), ('2025/07/CEFund-and-Hamilton-logo-black.webp', 'City Enrichment Fund, City of Hamilton')]

logos = ('<!-- wp:group {"className":"ncah-logos","layout":{"type":"flex","flexWrap":"wrap","justifyContent":"center","verticalAlignment":"center"}} -->\n<div class="wp-block-group ncah-logos">'
         + '\n\n'.join(logo(U + p, a) for p, a in partners) + '</div>\n<!-- /wp:group -->')
out.append(band(heading('Our partners', 2, '', 'center', 'x-large') + '\n\n' +
                para('We would like to extend our heartfelt gratitude to the following organizations and individuals for their generous support. Your contributions have made a significant impact on our community and enabled us to continue promoting Nigerian culture and heritage in Canada.', align='center') + '\n\n' + logos, 'mist', 'ncah-partners'))


write('home.html', out)
