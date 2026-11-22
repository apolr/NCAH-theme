"""Builds content/home.html (the Welcome page) as native WordPress blocks.
Content and image URLs come from the live Elementor page 359 (read only export, Nov 22, 2026).
Run: python3 tools/build_home.py
"""
import html, json, pathlib

U = 'https://ncahamilton.ca/wp-content/uploads/'
e = lambda t: html.escape(t, quote=False)
j = lambda d: json.dumps(d, separators=(',', ':'))

def heading(text, level=2, cls='', align=None, size=None, color=None):
    a = {}
    c = ['wp-block-heading']
    if level != 2: a['level'] = level
    if align: a['textAlign'] = align; c.append(f'has-text-align-{align}')
    if cls: a['className'] = cls; c.append(cls)
    if size: a['fontSize'] = size; c.append(f'has-{size}-font-size')
    if color: a['textColor'] = color; c += [f'has-{color}-color', 'has-text-color']
    return f'<!-- wp:heading {j(a)} -->\n<h{level} class="{" ".join(c)}">{e(text)}</h{level}>\n<!-- /wp:heading -->'

def para(text, cls='', align=None, size=None, color=None, raw=False):
    a = {}
    c = []
    if align: a['align'] = align; c.append(f'has-text-align-{align}')
    if cls: a['className'] = cls; c.append(cls)
    if size: a['fontSize'] = size; c.append(f'has-{size}-font-size')
    if color: a['textColor'] = color; c += [f'has-{color}-color', 'has-text-color']
    cl = f' class="{" ".join(c)}"' if c else ''
    return f'<!-- wp:paragraph {j(a)} -->\n<p{cl}>{text if raw else e(text)}</p>\n<!-- /wp:paragraph -->'

def button(label, url, red=False):
    a = {'backgroundColor': 'ncah-red', 'textColor': 'white'} if red else {}
    cl = 'wp-block-button__link has-white-color has-ncah-red-background-color has-text-color has-background wp-element-button' if red else 'wp-block-button__link wp-element-button'
    return (f'<!-- wp:button {j(a)} -->\n<div class="wp-block-button"><a class="{cl}" href="{html.escape(url)}">{e(label)}</a></div>\n<!-- /wp:button -->')

def buttons(items, center=True, cls=''):
    a = {}
    if cls: a['className'] = cls
    if center: a['layout'] = {'type': 'flex', 'justifyContent': 'center'}
    c = 'wp-block-buttons' + (f' {cls}' if cls else '')
    return f'<!-- wp:buttons {j(a)} -->\n<div class="{c}">' + '\n\n'.join(items) + '</div>\n<!-- /wp:buttons -->'

def slide(img, title, label, url, red=False):
    inner = []
    if title: inner.append(heading(title, 2, 'ncah-rise', 'center', 'hero', 'white'))
    inner.append(buttons([button(label, url, red)], cls='ncah-rise'))
    a = {'url': img, 'dimRatio': 40, 'align': 'full', 'className': 'ncah-hero__slide', 'minHeight': 80, 'minHeightUnit': 'vh',
         'contentPosition': 'bottom center' if not title else 'center center'}
    return (f'<!-- wp:cover {j(a)} -->\n<div class="wp-block-cover alignfull ncah-hero__slide" style="min-height:80vh">'
            f'<span aria-hidden="true" class="wp-block-cover__background has-background-dim-40 has-background-dim"></span>'
            f'<img class="wp-block-cover__image-background" alt="" src="{img}" data-object-fit="cover"/>'
            f'<div class="wp-block-cover__inner-container">' + '\n\n'.join(inner) + '</div></div>\n<!-- /wp:cover -->')

def card(img, title, text):
    """Image background card with a dark panel, as on the live Welcome page."""
    a = {'url': img, 'dimRatio': 20, 'minHeight': 300, 'isDark': True, 'style': {'border': {'radius': '20px'}}}
    return (f'<!-- wp:cover {j(a)} -->\n<div class="wp-block-cover is-light has-custom-border" style="border-radius:20px;min-height:300px">'
            f'<span aria-hidden="true" class="wp-block-cover__background has-background-dim-20 has-background-dim"></span>'
            f'<img class="wp-block-cover__image-background" alt="" src="{img}" data-object-fit="cover"/>'
            f'<div class="wp-block-cover__inner-container">'
            '<!-- wp:group {"style":{"color":{"background":"#0000009c"},"border":{"radius":"20px"},"spacing":{"padding":{"top":"2rem","bottom":"2rem","left":"2rem","right":"2rem"}}},"layout":{"type":"default"}} -->\n'
            '<div class="wp-block-group has-background" style="border-radius:20px;background-color:#0000009c;padding:2rem">'
            + heading(title, 2, '', None, 'x-large', 'white') + '\n\n' + para(text, color='white') +
            '</div>\n<!-- /wp:group --></div></div>\n<!-- /wp:cover -->')

def column(content, width=None):
    a = {'width': width} if width else {}
    st = f' style="flex-basis:{width}"' if width else ''
    return f'<!-- wp:column {j(a)} -->\n<div class="wp-block-column"{st}>{content}</div>\n<!-- /wp:column -->'

def columns(cols, cls=''):
    a = {'className': cls} if cls else {}
    c = 'wp-block-columns' + (f' {cls}' if cls else '')
    return f'<!-- wp:columns {j(a)} -->\n<div class="{c}">' + '\n\n'.join(cols) + '</div>\n<!-- /wp:columns -->'

def band(inner, bg=None, cls='', width='1250px'):
    a = {'align': 'full', 'layout': {'type': 'constrained', 'contentSize': width}, 'className': ('ncah-reveal ' + cls).strip(),
         'style': {'spacing': {'padding': {'top': '3rem', 'bottom': '3rem'}}}}
    c = 'wp-block-group alignfull ' + a['className']
    if bg: a['backgroundColor'] = bg; c += f' has-{bg}-background-color has-background'
    return (f'<!-- wp:group {j(a)} -->\n<div class="{c}" style="padding-top:3rem;padding-bottom:3rem">' + inner + '</div>\n<!-- /wp:group -->')

def youtube(url, caption):
    return (f'<!-- wp:embed {j({"url": url, "type": "video", "providerNameSlug": "youtube", "responsive": True, "className": "wp-embed-aspect-16-9 wp-has-aspect-ratio"})} -->\n'
            f'<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">\n{url}\n</div><figcaption class="wp-element-caption">{e(caption)}</figcaption></figure>\n<!-- /wp:embed -->')

def logo(src, alt):
    return f'<!-- wp:image {{"sizeSlug":"medium","linkDestination":"none"}} -->\n<figure class="wp-block-image size-medium"><img src="{src}" alt="{html.escape(alt)}"/></figure>\n<!-- /wp:image -->'

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
