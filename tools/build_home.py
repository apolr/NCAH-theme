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
hero_inner = (heading('Celebrating Heritage. Fostering Interactions. Providing Support.', 1, '', 'center', 'hero', 'white') + '\n\n' +
              buttons([button('Learn more', '/about-us/', True)]))
hero_cover = cover(U + '2026/10/DSC_6472-scaled.webp', hero_inner, 'ncah-hero1 alignfull ncah-hero__slide', 20, 720, 'bottom center').replace('wp-block-cover is-dark', 'wp-block-cover alignfull is-dark', 1)

# 1a. Annual Gala flyer slide: first slide, image only plus one ticket button. Removed automatically after Dec 5, 2026 (see functions.php).
FLYER = U + '2026/10/IMG_3257-2048x1026.webp'
FLYER_TALL = '/wp-content/themes/ncah/assets/img/gala-flyer-portrait.webp'
gala_alt = '5V5, Honouring Our Root, Annual Gala. December 5, 2026, red carpet 4 PM, party 5 PM, The Grand Olympia, Stoney Creek.'
gala_slide = ('<!-- wp:group {"className":"ncah-hero__slide ncah-gala-slide","layout":{"type":"flex","orientation":"vertical","justifyContent":"center"}} -->\n'
              '<div class="wp-block-group ncah-hero__slide ncah-gala-slide">'
              '<!-- wp:image {"sizeSlug":"full","className":"ncah-gala-flyer ncah-gala-flyer--wide"} -->\n'
              f'<figure class="wp-block-image size-full ncah-gala-flyer ncah-gala-flyer--wide"><img src="{FLYER}" alt="{gala_alt}"/></figure>\n<!-- /wp:image -->\n\n'
              '<!-- wp:image {"sizeSlug":"full","className":"ncah-gala-flyer ncah-gala-flyer--tall"} -->\n'
              f'<figure class="wp-block-image size-full ncah-gala-flyer ncah-gala-flyer--tall"><img src="{FLYER_TALL}" alt="{gala_alt}" width="1280" height="1600"/></figure>\n<!-- /wp:image -->\n\n'
              + buttons([button('Get your tickets', 'https://www.zeffy.com/en-CA/ticketing/annual-gala-8173', True)], cls='ncah-gala-cta') +
              '</div>\n<!-- /wp:group -->')
out.append('<!-- wp:group {"align":"full","className":"ncah-hero ncah-home-hero","layout":{"type":"default"}} -->\n<div class="wp-block-group alignfull ncah-hero ncah-home-hero">\n' + gala_slide + '\n\n' + hero_cover + '</div>\n<!-- /wp:group -->')

# 2. Get involved: four photo tiles
def tile(img, title, text, url, extra=''):
    inner = heading(title, 3, '', None, None, 'white') + '\n\n' + para(text, size='small', color='white')
    return column(f'<a href="{url}" class="ncah-tile-link">' + cover(img, inner, 'ncah-tile' + extra, 35, 340, 'bottom left') + '</a>')
tiles = columns([
    tile(U + '2026/11/child-with-nigerian-flag.webp', 'About us', 'Learn more about the Community.', '/about-us/', ' ncah-tile--portrait'),
    tile(U + '2023/12/settlement.webp', 'Membership', 'Join a thriving community and participate.', '/membership/'),
    tile(U + '2026/11/ethnic-food-bank-programs.webp', 'Programs', 'Our programs are poised to support the community.', '/programs/'),
    tile(U + '2023/12/The-Nigerian-Spirit-1.webp', 'Donate', 'Your support keeps the spirit alive.', '/donate/'),
], 'ncah-tiles')
out.append('<!-- wp:group {"align":"full","layout":{"type":"default"}} -->\n<div class="wp-block-group alignfull">' + tiles + '</div>\n<!-- /wp:group -->')

# 3. Membership: green band, brief intro, six perk cards
perks = [('Connect', 'Meet professionals and neighbours, and stay informed on community news.'),
         ('Engage', 'Join events and activities that celebrate Nigerian culture.'),
         ('Learn', 'Workshops, virtual clinics and resources for growth.'),
         ('Support', 'Help in hard times, and a chance to help others.'),
         ('Lead', 'Take on leadership roles and help shape our direction.'),
         ('Have a voice', 'Have a say in decisions that shape the association.')]
ICONS = ['<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
         '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
         '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
         '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21.3l7.8-7.8 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
         '<path d="M4 22V4"/><path d="M4 4h13l-2 4 2 4H4"/>',
         '<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.5 8.5 0 0 1-3.8-.9L3 21l1.9-5.2A8.4 8.4 0 1 1 21 11.5z"/>']
def perk(n, t, d):
    ico = ('<!-- wp:html -->\n<span class="ncah-perk__n" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
           + ICONS[n - 1] + '</svg></span>\n<!-- /wp:html -->')
    return ('<!-- wp:group {"className":"ncah-perk","layout":{"type":"default"}} -->\n<div class="wp-block-group ncah-perk">'
            + ico + '\n\n' + heading(t, 3, 'ncah-perk__t') + '\n\n' + para(d, 'ncah-perk__d') + '</div>\n<!-- /wp:group -->')
four = ('<!-- wp:group {"className":"ncah-perks","layout":{"type":"default"}} -->\n<div class="wp-block-group ncah-perks">'
        + '\n\n'.join(perk(i + 1, t, d) for i, (t, d) in enumerate(perks)) + '</div>\n<!-- /wp:group -->')
memtext = 'Voluntary and open to all peoples of Nigeria by birth, naturalization, marriage or heritage, and to others who share our principles.'
mem = (columns([column(heading('Become a Member', 2, '', None, 'x-large', 'white') + '\n\n' + para(memtext, color='white'), '70%'),
                column(buttons([button('Register today', '/membership/', True)], center=False), '30%')]) + '\n\n' + four)
out.append(band(mem, None, 'ncah-green-band ncah-membership'))

# 4. Upcoming event: the Gala (creative split, same system as About us)
gala = assoc_section(U + '2026/10/IMG_3257-scaled.webp', '2026 NCAH Annual Gala', 'Upcoming event', '2026 NCAH Annual Gala: 5v5!',
    'Join us for the 2026 NCAH Annual Gala at Grand Olympia, Stoney Creek.',
    ['Saturday, December 5, 2026', '5 PM', 'Theme: 5v5!'], 'Dec', '5',
    extra=buttons([button('Get your tickets', 'https://www.zeffy.com/en-CA/ticketing/annual-gala-8173', True)], center=False), img_cls='ncah-assoc__img--poster')
out.append(band(gala, None, 'ncah-upcoming'))

# 5. Green Spirit Initiative and video (video right on desktop)
gsi = assoc_section(U + '2026/09/Back-to-School-Supplies-9.webp', 'Volunteers smiling as they unload donated backpacks and school supplies from a car', 'Green Spirit Initiative', 'The charitable arm of the NCAH',
    'The Green Spirit Initiative (GSI) is the charitable arm of the NCAH, dedicated to empowering visible minorities and newcomers through community-focused support. Inspired by the Nigerian flag, the initiative focuses on improving social determinants of health to build a more inclusive and prosperous society.',
    ['Empowering newcomers', 'Visible minorities', 'Social determinants of health'], 'Charity', 'GSI', rev=True,
    extra=buttons([button('Donate', '/donate/', True)], center=False))
out.append(band(gsi, 'mist', 'ncah-gsi'))

# 5b. Golden Eagles
ge = assoc_section(U + '2026/10/DSC_7787.webp', 'Golden Eagles of Hamilton', 'Community soccer', 'Golden Eagles, Winners 2026 Hamilton AFCON',
    'Our community soccer team. Visit the Golden Eagles site for news, fixtures and the squad.',
    ['News', 'Fixtures', 'The squad'], 'Winners', '2026',
    extra=buttons([button('Discover Golden Eagles', 'https://soccer.ncahamilton.ca/', True)], center=False))
out.append(band(ge, None, 'ncah-golden'))

# 6. News: latest posts
q = ('<!-- wp:query {"query":{"perPage":3,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","inherit":false},"className":"ncah-events"} -->\n'
     '<div class="wp-block-query ncah-events"><!-- wp:post-template {"layout":{"type":"grid","columnCount":3}} -->\n'
     '<!-- wp:post-featured-image {"isLink":true,"aspectRatio":"4/3"} /-->\n\n<!-- wp:post-date /-->\n\n'
     '<!-- wp:post-title {"level":3,"isLink":true,"fontSize":"large"} /-->\n<!-- /wp:post-template --></div>\n<!-- /wp:query -->')
out.append(band(heading('News and Events', 2, '', 'center', 'x-large') + '\n\n' + q + '\n\n' + buttons([button('View the Event Gallery', '/event-gallery/', True)]), None, 'ncah-news'))

# 7. Videos (first three; the rest can live on a Gallery page later)
from build_home_vids import VIDS as vids

grid = ('<!-- wp:group {"className":"ncah-watch","layout":{"type":"grid","columnCount":3}} -->\n<div class="wp-block-group ncah-watch">'
        + '\n\n'.join(youtube(u, t) for t, u in vids[:3]) + '</div>\n<!-- /wp:group -->')
out.append(band(heading('NCAH TV', 2, '', 'center', 'x-large') + '\n\n' + grid + '\n\n' + buttons([button('More videos', '/gallery/', True)]), 'mist', 'ncah-videos'))

# 8. Partners
partners = [('2025/12/ACCA.webp', 'ACCA'), ('2026/11/Black-AI-Centre.webp', 'Black AI Centre'), ('2025/12/Davisol.webp', 'Davisol'), ('2025/12/Hamilton-Urban-Core.webp', 'Hamilton Urban Core'),
            ('2025/12/HBHCLF.webp', 'Hamilton Black Health Community Leaders Forum'), ('2025/12/Isreal-Iyamu.webp', 'Israel Iyamu'),
            ('2025/12/Refune-Newcomer-Health.webp', 'Refuge Newcomer Health'), ('2026/11/Your-Area-Dental.webp', 'Your Area Dental'), ('2026/11/CEFund-and-Hamilton-logo-blue.webp', 'City Enrichment Fund, City of Hamilton')]

logos = ('<!-- wp:group {"className":"ncah-logos","layout":{"type":"flex","flexWrap":"wrap","justifyContent":"center","verticalAlignment":"center"}} -->\n<div class="wp-block-group ncah-logos">'
         + '\n\n'.join(logo(U + p, a) for p, a in partners) + '</div>\n<!-- /wp:group -->')
out.append(band(heading('Our partners', 2, '', 'center', 'x-large') + '\n\n' +
                para('Thank you to the organizations and individuals whose generous support makes our work possible.', align='center') + '\n\n' + logos, 'mist', 'ncah-partners'))


write('home.html', out)
