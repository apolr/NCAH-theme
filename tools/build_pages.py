"""Builds content/about-us.html, membership.html, events.html, contact-us.html as native blocks.
Content from the live Elementor pages 488, 799, 1167, 802 (read only export, Nov 22, 2026).
Run: python3 -I tools/build_pages.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ncah_blocks import *

def sec(inner, bg=None, cls='', anchor=None):
    return band(inner, bg, cls)

# ---------- About us ----------
a = [page_head('About us', U + '2026/10/DSC_6531-scaled.webp', focus_y=0.3, extra_cls='ncah-head-group')]
a.append(band(assoc_section(U + '2025/07/118A9755-scaled.webp', 'Families and community members gathered under tents at an NCAH community event', 'Who we are', 'The Association',
    'The Nigerian Canadian Association, Hamilton and Environs (NCAH) is a non-profit organization founded in 1999. We support youth to embrace their heritage, pursue academic success and develop their creativity.',
    ['Heritage', 'Academic success', 'Creativity']),
    None, 'ncah-about-association'))
a.append(band(assoc_section(U + '2026/09/Back-to-School-Supplies-9.webp', 'NCAH volunteers smiling as they unload donated backpacks and school supplies from a car', 'Why we exist', 'Our Mission',
    'Our mission is to promote unity and provide a conducive environment for individuals with Nigerian heritage to thrive in the community.',
    ['Unity', 'Conducive environment', 'Thrive in community'], 'Promoting', 'Unity', rev=True),
    'mist', 'ncah-about-mission'))
goals = ['Enrich Canadian culture with subtle infusions of Nigerian traditions.',
         'Create a welcoming hub for diverse social interaction.',
         'Connect children of Nigerian heritage (and others) to their cultural roots.',
         'Provide essential support to members in need.',
         'Enhance social and economic well-being for members and the community.']
GI = ['<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8-6.2-3.3-6.2 3.3L8 14.2 3 9.3l6.9-1z"/>',
      '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
      '<path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/><path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/>',
      '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="m4.93 4.93 4.24 4.24M14.83 9.17l4.24-4.24M14.83 14.83l4.24 4.24M9.17 14.83l-4.24 4.24"/>',
      '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>']
def goal(i, g):
    ico = ('<!-- wp:html -->\n<span class="ncah-goal__ico" aria-hidden="true"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + GI[i] + '</svg></span>'
           f'<span class="ncah-goal__num" aria-hidden="true">{i + 1:02d}</span>\n<!-- /wp:html -->')
    return ('<!-- wp:group {"className":"ncah-goal","layout":{"type":"default"}} -->\n<div class="wp-block-group ncah-goal">' + ico + '\n\n' + para(g, 'ncah-goal__t') + '</div>\n<!-- /wp:group -->')
lst = ('<!-- wp:group {"className":"ncah-goals","layout":{"type":"default"}} -->\n<div class="wp-block-group ncah-goals">' + '\n\n'.join(goal(i, g) for i, g in enumerate(goals)) + '</div>\n<!-- /wp:group -->')
a_ = band(section_title('What we work toward', 'Our Goals') + '\n\n' + lst, 'ncah-green', 'ncah-green-band ncah-about-goals', '1200px')
a.append(a_)

execs = [('Chuma Okereke', 'President', 'president'),
         ('Ifeoluwa Akande', 'Vice President', 'vp'),
         ('Emeka Diru', 'Program Director, Administration', 'secretary'),
         ('Augustine Ubimago', 'Program Director, Socials', 'socialsec'),
         ('Kayode Atobatele', 'Program Director, Public Relations', 'pro'),
         ('Ijeoma Igboeli', 'Program Director, Finance', 'finsec'),
         ('Yvonne Ekama', 'Program Director, Treasury', 'treasurer'),
         ('Kingsley Maduike', 'Program Director, Protocol and Logistics', 'provost'),
         ('Diepriye Opuda', 'Program Director, Youth and Sports', 'ysd')]
PHOTOS = {'president': '2026/05/Chukwuma-Okereke-819x1024.webp', 'vp': '2026/05/Dr-Ife-819x1024.webp', 'secretary': '2026/05/Emeka-Diru-819x1024.webp', 'socialsec': '2026/05/Augustine-Ubimago_-819x1024.webp', 'pro': '2026/05/Kayode-Ayobatele-819x1024.webp', 'finsec': '2026/10/Ms.-Ijeoma-Igboeli-819x1024.webp', 'treasurer': '2026/05/Yvonne-Ekama-819x1024.webp', 'provost': '2026/05/Kingsley-Maduike-819x1024.webp', 'ysd': '2023/12/Vice-President.webp'}
def exec_card(n, r, m):
    mail = f'{m}@ncahamilton.ca'
    return ('<!-- wp:group {"className":"ncah-exec","style":{"spacing":{"padding":{"top":"1.5rem","bottom":"1.5rem","left":"1.5rem","right":"1.5rem"}},"border":{"radius":"12px"}},"backgroundColor":"white","layout":{"type":"default"}} -->\n'
            '<div class="wp-block-group ncah-exec has-white-background-color has-background" style="border-radius:12px;padding:1.5rem">'
            f'<!-- wp:image {{"sizeSlug":"large","className":"ncah-exec-photo"}} -->\n<figure class="wp-block-image size-large ncah-exec-photo"><img src="{U}{PHOTOS[m]}" alt="{n}, {r}"/></figure>\n<!-- /wp:image -->' + heading(n, 3, '', None, 'medium', 'ncah-green') + '\n\n' + para(r, size='small') + '\n\n' +
            para(f'<a href="mailto:{mail}">{mail}</a>', size='small', raw=True) + '</div>\n<!-- /wp:group -->')
grid = '<!-- wp:group {"className":"ncah-exec-grid","layout":{"type":"grid","columnCount":3}} -->\n<div class="wp-block-group ncah-exec-grid">' + '\n\n'.join(exec_card(*x) for x in execs) + '</div>\n<!-- /wp:group -->'
a.append(band('<!-- wp:group {"anchor":"executives"} --><div id="executives" class="wp-block-group">' + section_title('Leadership', 'Meet the Executives') + '\n\n' + grid + '</div><!-- /wp:group -->', None, 'ncah-executives'))
a.append(band(split(U + '2024/05/NCAH-Contsitution-and-Bye-law.webp', 'Our Foundations', 'Constitution and By-Laws',
    'Explore the guiding principles and regulations that shape the Nigerian Canadian Association, Hamilton. Our Constitution and By-Laws provide the framework for our operations, governance, and community engagement, ensuring transparency, accountability, and fairness in all we do. This section offers insight into how we uphold our values and manage our association for the benefit of all members.', False,
    buttons([button('Download', U + '2026/02/NCA-Hamilton-Bylaws-Signed.pdf', True).replace('href=', 'target="_blank" rel="noopener" href=')], center=False)), 'mist', 'ncah-foundations'))
write('about-us.html', a)

# ---------- Membership ----------
m = [page_head('Membership', U + '2025/07/118A9755-scaled.webp', focus_y=0.5, extra_cls='ncah-head-crowd')]
def flow_step(n, t, d):
    return ('<!-- wp:group {"className":"ncah-flow__step","layout":{"type":"default"}} -->\n<div class="wp-block-group ncah-flow__step">'
            + para(n, 'ncah-flow__n') + '\n\n' + heading(t, 3, 'ncah-flow__t') + '\n\n' + para(d, 'ncah-flow__d') + '</div>\n<!-- /wp:group -->')
steps = [('01', 'Apply', 'Complete the form below: full name, Canadian WhatsApp number, address and who referred you.'),
         ('02', 'Verified', 'An administrator verifies your address.'),
         ('03', 'Invited', 'You receive an invitation to the NCAH WhatsApp Community.')]
flow = ('<!-- wp:group {"className":"ncah-flow","layout":{"type":"default"}} -->\n<div class="wp-block-group ncah-flow">' + '\n\n'.join(flow_step(*x) for x in steps) + '</div>\n<!-- /wp:group -->')
intro = (para('Membership', 'ncah-eyebrow', 'center', None, 'ncah-red') + '\n\n' + heading('Join the NCAH community', 2, '', 'center', 'x-large') + '\n\n' +
         para('Open to all peoples of Nigeria by birth, naturalization, marriage or heritage, and to others who share our principles. Members join the NCAH WhatsApp Community for announcements, events and programs.', 'ncah-flow__lead', 'center') + '\n\n' +
         para('Serving Hamilton-Wentworth, Burlington, Oakville, Kitchener, Waterloo, Guelph, Grimsby and St. Catharines.', 'ncah-flow__where', 'center'))
cta = ('<!-- wp:group {"className":"ncah-flow__cta","layout":{"type":"default"}} -->\n<div class="wp-block-group ncah-flow__cta">'
       '<!-- wp:group {"layout":{"type":"default"}} -->\n<div class="wp-block-group">' + para('No membership fee.', 'ncah-flow__free') + '\n\n' +
       para('Giving is optional: tick the donor box on the form to give monthly, quarterly, bi-annually or annually. Donations support our charitable work and are never required.', 'ncah-flow__giving') + '</div>\n<!-- /wp:group -->\n\n' +
       buttons([button('Request to join', '#join', True)], center=False) + '</div>\n<!-- /wp:group -->')
m.append(band(intro + '\n\n' + flow + '\n\n' + cta, 'mist', 'ncah-member-flow', '1100px'))
m.append(band('<!-- wp:html -->\n<div id="join"></div>\n<!-- /wp:html -->\n\n' + section_title('Membership form', 'Request to join') + '\n\n<!-- wp:shortcode -->\n[ncah_member_form]\n<!-- /wp:shortcode -->', None, 'ncah-member-form-band', '760px'))
write('membership.html', m)

# ---------- Events ----------
q = ('<!-- wp:query {"query":{"perPage":12,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","inherit":false},"className":"ncah-events ncah-event-gallery"} -->\n'
     '<div class="wp-block-query ncah-events ncah-event-gallery"><!-- wp:post-template {"layout":{"type":"grid","columnCount":3}} -->\n'
     '<!-- wp:post-featured-image {"isLink":true,"aspectRatio":"4/3"} /-->\n\n<!-- wp:post-date {"fontSize":"small"} /-->\n\n'
     '<!-- wp:post-title {"level":3,"isLink":true,"fontSize":"medium"} /-->\n\n<!-- wp:post-excerpt {"excerptLength":20} /-->\n<!-- /wp:post-template -->\n\n'
     '<!-- wp:query-pagination {"layout":{"type":"flex","justifyContent":"center"}} -->\n<!-- wp:query-pagination-previous /-->\n\n<!-- wp:query-pagination-numbers /-->\n\n<!-- wp:query-pagination-next /-->\n<!-- /wp:query-pagination -->'
     '</div>\n<!-- /wp:query -->')
tabs = '<!-- wp:shortcode -->\n[ncah_year_tabs]\n<!-- /wp:shortcode -->'
write('event-gallery.html', [page_head('Event Gallery', U + '2023/07/IMG-20230730-WA0012.webp'), band(tabs + '\n\n' + q, None, 'ncah-events-band'),
    band('<!-- wp:html -->\n<div id="videos"></div>\n<!-- /wp:html -->\n\n' + section_title('Watch', 'Videos') + '\n\n' + para('Recaps and highlights from our YouTube channel.', align='center') + '\n\n<!-- wp:shortcode -->\n[ncah_videos]\n<!-- /wp:shortcode -->', 'mist', 'ncah-videos-band')])

# ---------- Contact Us ----------
c = [page_head('Contact Us', U + '2024/01/contact-us.webp')]
ICON_WA = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>'
ICON_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>'
def action(cls, href, icon, title, sub, ext=False):
    t = ' target="_blank" rel="noopener"' if ext else ''
    return (f'<a class="ncah-action {cls}" href="{href}"{t}><span class="ncah-action__icon">{icon}</span>'
            f'<span class="ncah-action__text"><strong>{title}</strong><small>{sub}</small></span>'
            '<span class="ncah-action__arrow" aria-hidden="true">&rarr;</span></a>')
ICON_PIN = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 010-5 2.5 2.5 0 010 5z"/></svg>'
ADDR = 'Suite 124 4-168 Barton Street, Stoney Creek ON L8E 4V6'
ADDR_Q = 'Suite%20124%204-168%20Barton%20Street%2C%20Stoney%20Creek%20ON%20L8E%204V6'
card = ('<div class="ncah-contact-card"><p class="ncah-eyebrow">Reach us</p><h3 class="ncah-contact-card__title">Talk to the NCAH team</h3>'
        '<div class="ncah-contact-actions">'
        + action('ncah-action--wa', 'https://wa.me/12892442568?text=Hello%20NCAH%2C%20I%20would%20like%20to%20get%20in%20touch.', ICON_WA, 'Chat on WhatsApp', 'Start an instant chat with the NCAH team', True)
        + action('ncah-action--tel', 'tel:+12892442568', ICON_TEL, 'Give us a call', '+1 (289) 244-2568')
        + action('ncah-action--mail', 'mailto:info@ncahamilton.ca', ICON_MAIL, 'Send us an Email', 'info@ncahamilton.ca')
        + f'<div class="ncah-action ncah-action--pin ncah-action--static"><span class="ncah-action__icon">{ICON_PIN}</span>'
        f'<span class="ncah-action__text"><strong>Mailbox address</strong><small>{ADDR}</small></span></div>'
        '</div>'
        '<div class="ncah-contact-social"><p class="ncah-contact-social__label">Follow us</p><div class="ncah-contact-social__links">'
        '<a href="https://www.facebook.com/NCAHamilton" target="_blank" rel="noopener">Facebook</a>'
        '<a href="https://www.instagram.com/ncahamilton/" target="_blank" rel="noopener">Instagram</a>'
        '<a href="https://www.youtube.com/@NCAHamilton" target="_blank" rel="noopener">YouTube</a></div></div></div>')
mapb = (f'<div class="ncah-contact-map"><iframe title="Map showing the location of the NCAH mailbox at {ADDR}" src="https://maps.google.com/maps?q={ADDR_Q}&amp;z=16&amp;output=embed" '
        'loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>'
        f'<div class="ncah-contact-map__bar"><span class="ncah-contact-map__addr">{ICON_PIN}<span>Mailbox address: {ADDR}</span></span></div></div>')
c.append(band('<!-- wp:html -->\n<div class="ncah-contact-grid">' + card + mapb + '</div>\n<!-- /wp:html -->', 'mist', 'ncah-contact-info', '1200px'))
write('contact-us.html', c)

# ---------- Donate ----------
d = [page_head('Donate', U + '2024/01/contact-us.webp'),
     band(section_title('Give', 'Support NCAH') + '\n\n' +
          para('Your gift supports our community programs and the Youth and Sports Directorate. Donations are made securely through Zeffy. Official donation receipts are issued by NCAH for eligible gifts, in line with our bylaws and Canada Revenue Agency rules. Questions about receipts? Email info@ncahamilton.ca.') + '\n\n' +
          '<!-- wp:shortcode -->\n[zeffy-donate fullwidth=true height=1100]\n<!-- /wp:shortcode -->', None, 'ncah-donate', '800px')]
write('donate.html', d)

# ---------- Programs (one page, all programs as cards) ----------
PROGS = [
    dict(id='family-fun-festival', title='Family Fun Festival', img=U + '2026/07/IMGL0574-scaled.webp',
         desc='A community celebration that promotes multicultural awareness and community integration.',
         more='A community celebration that promotes multicultural awareness and community integration. Browse photos from past festivals and picnics, or watch the highlights.',
         links=[('View event gallery', '/category/summer-picnic/', True), ('Watch videos', '/gallery/', False)]),
    dict(id='annual-gala', title='Annual Gala', img=U + '2025/02/MACL3788-scaled.webp',
         desc='Our annual gala brings the community together and raises funds for our charitable programs.',
         more='Our annual gala brings the community together and raises funds for our charitable programs. The 2026 theme is 5v5, on December 5, 2026 at Grand Olympia, Stoney Creek.',
         links=[('View event gallery', '/category/end-of-the-year-gala/', True), ('Watch videos', '/gallery/', False), ('Get your tickets', 'https://www.zeffy.com/en-CA/ticketing/annual-gala-8173', False)]),
    dict(id='ethnic-food-bank', title='Ethnic Food Bank', img=U + '2026/10/Ethnic-Food-Bank-6.webp',
         desc='Food support and resource referrals for low-income individuals and families in Hamilton and surrounding areas.',
         more='Food support and resource referrals for low-income individuals and families in Hamilton and surrounding areas.',
         links=[('View event gallery', '/category/ethnic-food-bank/', True)]),
    dict(id='golden-eagles', title='Golden Eagles of Hamilton', img=U + '2026/10/DSC_7787.webp',
         desc='Our community soccer team. Visit the Golden Eagles site for news, fixtures and the squad.', href='https://soccer.ncahamilton.ca/'),
]
def pcard(d):
    img = f'<span class="ncah-pcard__img"><img src="{d["img"]}" alt="" loading="lazy" decoding="async"></span>'
    if 'href' in d:
        return (f'<a class="ncah-pcard" href="{d["href"]}" target="_blank" rel="noopener">{img}<span class="ncah-pcard__body"><strong class="ncah-pcard__t">{e(d["title"])}</strong>'
                f'<span class="ncah-pcard__d">{e(d["desc"])}</span><span class="ncah-pcard__cta">Visit website <span aria-hidden="true">&#8599;</span></span></span></a>')
    return (f'<button type="button" class="ncah-pcard" data-modal="pm-{d["id"]}" aria-haspopup="dialog">{img}<span class="ncah-pcard__body"><strong class="ncah-pcard__t">{e(d["title"])}</strong>'
            f'<span class="ncah-pcard__d">{e(d["desc"])}</span><span class="ncah-pcard__cta">Learn more <span aria-hidden="true">&rarr;</span></span></span></button>')
def pmodal(d):
    if 'href' in d: return ''
    links = ''.join(f'<a class="ncah-pmodal__btn{"" if first else " is-alt"}" href="{h}"{" target=_blank rel=noopener" if h.startswith("http") else ""}>{e(t)}</a>' for (t, h, first) in d['links'])
    return (f'<dialog class="ncah-pmodal" id="pm-{d["id"]}" aria-labelledby="pm-{d["id"]}-t"><button type="button" class="ncah-pmodal__x" aria-label="Close">&times;</button>'
            f'<img class="ncah-pmodal__img" src="{d["img"]}" alt="" loading="lazy"><div class="ncah-pmodal__body"><h3 id="pm-{d["id"]}-t">{e(d["title"])}</h3><p>{e(d["more"])}</p>'
            f'<div class="ncah-pmodal__links">{links}</div></div></dialog>')
PJS = ("<script>(function(){var r=document.currentScript.parentNode;"
       "r.querySelectorAll('[data-modal]').forEach(function(b){b.addEventListener('click',function(){var d=document.getElementById(b.getAttribute('data-modal'));if(d&&d.showModal){d.showModal();d.dataset.from=b.getAttribute('data-modal');}});});"
       "r.querySelectorAll('dialog.ncah-pmodal').forEach(function(d){d.addEventListener('click',function(ev){if(ev.target===d||ev.target.classList.contains('ncah-pmodal__x')){d.close();}});"
       "d.addEventListener('close',function(){var b=r.querySelector('[data-modal=\"'+d.id+'\"]');if(b){b.focus();}});});})();</script>")
pg = '<div class="ncah-programs-page"><div class="ncah-pgrid">' + ''.join(pcard(d) for d in PROGS) + '</div>' + ''.join(pmodal(d) for d in PROGS) + PJS + '</div>'
write('programs.html', [page_head('Our programs', U + '2023/07/IMG-20230730-WA0012.webp', eyebrow='What we do', sub='Explore what NCAH runs for the community. Select a program to learn more.'),
    band('<!-- wp:html -->\n' + pg + '\n<!-- /wp:html -->', None, 'ncah-programs-band', '1200px')])

# ---------- Gallery (all videos) ----------
from build_home_vids import VIDS
gg = ('<!-- wp:group {"className":"ncah-watch","layout":{"type":"grid","columnCount":3}} -->\n<div class="wp-block-group ncah-watch">' + '\n\n'.join(youtube(u, t) for t, u in VIDS) + '</div>\n<!-- /wp:group -->')
write('gallery.html', [page_head('Gallery', U + '2023/07/IMG-20230730-WA0012.webp'), band(section_title('Watch', 'NCAH videos') + '\n\n' + gg, None, 'ncah-gallery')])

# ---------- Business directory ----------
bd = [page_head('Business directory', U + '2023/12/settlement.webp'),
      band(section_title('Support local', 'Businesses in our community') + '\n\n' +
           para('Members of the Nigerian Canadian Association run businesses across Hamilton and Environs. Browse the directory to find services and products from members, and support them.', align='center') + '\n\n' +
           '<!-- wp:shortcode -->\n[ncah_business_directory]\n<!-- /wp:shortcode -->', None, 'ncah-directory-band', '1200px'),
      '<!-- wp:group {"align":"full","layout":{"type":"constrained","contentSize":"760px"},"className":"ncah-member-form-band ncah-biz-form-band","style":{"spacing":{"padding":{"top":"3rem","bottom":"3rem"}}}} -->\n'
      '<div class="wp-block-group alignfull ncah-member-form-band ncah-biz-form-band" style="padding-top:3rem;padding-bottom:3rem"><!-- wp:html -->\n<div id="request"></div>\n<!-- /wp:html -->\n\n' +
      para('Business directory request', 'ncah-eyebrow', 'center', None, 'ncah-red') + '\n\n' +
      heading('Request a listing', 2, '', 'center', 'x-large') + '\n\n' +
      para('Only registered NCAH members can list a business. Not a member yet? Choose "No, not yet" in the form to register first. Every request is verified and approved by an administrator.', align='center') + '\n\n' +
      '<!-- wp:shortcode -->\n[ncah_business_form]\n<!-- /wp:shortcode --></div>\n<!-- /wp:group -->']
write('business-directory.html', bd)
