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
lst = ('<!-- wp:list {"ordered":true} -->\n<ol class="wp-block-list">' +
       ''.join(f'<!-- wp:list-item -->\n<li>{e(g)}</li>\n<!-- /wp:list-item -->' for g in goals) + '</ol>\n<!-- /wp:list -->')
a.append(band(section_title('What we work toward', 'Our Goals') + '\n\n' + lst, 'ncah-green', 'ncah-green-band ncah-about-goals', '900px'))

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
m = [page_head('Membership', U + '2024/01/Google-Form-Header.webp')]
what = ('Membership of the Nigerian Canadian Association, Hamilton and Environs (NCAH) is how you join our community. '
        'Members are invited into the NCAH WhatsApp Community, where announcements, events and programs are shared. '
        'Registration is voluntary and open to all peoples of Nigeria by birth, naturalization, marriage or heritage, and to others committed to the principles of the Association.')
m.append(band(split(U + '2023/12/hi-res-be6cc83762096029bbf781b08a079cb8_crop_north-scaled.webp', 'What membership means', 'Join the NCAH community', what, extra=para('Membership is open to people from other regions and backgrounds who are committed to abiding by the principles and the established goals of the Association. The primary geographic regions that are encompassed in the activities of the Association are the Hamilton-Wentworth region and the surroundings, which include Burlington, Oakville, Kitchener, Waterloo, Guelph, Grimsby and St. Catharines.')), None, 'ncah-member-intro'))
def li(t): return f'<!-- wp:list-item -->\n<li>{e(t)}</li>\n<!-- /wp:list-item -->'
steps = ['Complete the form below with your full name, a Canadian WhatsApp number, your address and the name of the person who referred you.',
         'An administrator verifies your address.',
         'Once verified, you receive an invitation to the NCAH WhatsApp Community.',
         'Your registration is valid for one year from the month you register.']
ol = '<!-- wp:list {"ordered":true,"className":"ncah-steps"} -->\n<ol class="wp-block-list ncah-steps">' + '\n'.join(li(t) for t in steps) + '</ol>\n<!-- /wp:list -->'
donor = ('There is no membership fee. If you wish, you can also tick the donor box on the form and tell us how often you would like to give: monthly, quarterly, bi-annually or annually. '
         'Donations are voluntary and support our charitable work. They are not required to become a member.')
m.append(band(section_title('How it works', 'Four simple steps') + '\n\n' + ol + '\n\n' + heading('Giving is optional', 3) + '\n\n' + para(donor), 'mist', 'ncah-member-how', '900px'))
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
        + f'<a class="ncah-action ncah-action--pin" href="https://www.google.com/maps/search/?api=1&amp;query={ADDR_Q}" target="_blank" rel="noopener"><span class="ncah-action__icon">{ICON_PIN}</span>'
        f'<span class="ncah-action__text"><strong>Visit us</strong><small>{ADDR}</small></span><span class="ncah-action__arrow" aria-hidden="true">&rarr;</span></a>'
        '</div>'
        '<div class="ncah-contact-social"><p class="ncah-contact-social__label">Follow us</p><div class="ncah-contact-social__links">'
        '<a href="https://www.facebook.com/NCAHamilton" target="_blank" rel="noopener">Facebook</a>'
        '<a href="https://www.instagram.com/ncahamilton/" target="_blank" rel="noopener">Instagram</a>'
        '<a href="https://www.youtube.com/@NCAHamilton" target="_blank" rel="noopener">YouTube</a></div></div></div>')
mapb = (f'<div class="ncah-contact-map"><iframe title="Map showing the NCAH office at {ADDR}" src="https://maps.google.com/maps?q={ADDR_Q}&amp;z=16&amp;output=embed" '
        'loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>'
        f'<div class="ncah-contact-map__bar"><span class="ncah-contact-map__addr">{ICON_PIN}<span>{ADDR}</span></span>'
        f'<a class="ncah-contact-map__btn" href="https://www.google.com/maps/dir/?api=1&amp;destination={ADDR_Q}" target="_blank" rel="noopener">Get directions</a></div></div>')
c.append(band('<!-- wp:html -->\n<div class="ncah-contact-grid">' + card + mapb + '</div>\n<!-- /wp:html -->', 'mist', 'ncah-contact-info', '1200px'))
write('contact-us.html', c)

# ---------- Donate ----------
d = [page_head('Donate', U + '2024/01/contact-us.webp'),
     band(section_title('Give', 'Support NCAH') + '\n\n' +
          para('Your gift supports our community programs and the Youth and Sports Directorate. Donations are made securely through Zeffy. Official donation receipts are issued by NCAH for eligible gifts, in line with our bylaws and Canada Revenue Agency rules. Questions about receipts? Email info@ncahamilton.ca.') + '\n\n' +
          '<!-- wp:shortcode -->\n[zeffy-donate fullwidth=true height=1100]\n<!-- /wp:shortcode -->', None, 'ncah-donate', '800px')]
write('donate.html', d)

# ---------- Programs (one section per directorate) ----------
def dsec(slug, title, blurb):
    q = ('<!-- wp:query {"query":{"perPage":12,"postType":"program","order":"asc","orderBy":"title","inherit":false},"className":"ncah-programs ncah-dir-' + slug + '"} -->\n'
         '<div class="wp-block-query ncah-programs ncah-dir-' + slug + '"><!-- wp:post-template {"layout":{"type":"grid","columnCount":3}} -->\n'
         '<!-- wp:shortcode -->\n[ncah_status]\n<!-- /wp:shortcode -->\n\n'
         '<!-- wp:post-title {"level":3,"isLink":true,"fontSize":"medium"} /-->\n\n<!-- wp:post-excerpt {"excerptLength":24} /-->\n'
         '<!-- /wp:post-template -->\n\n<!-- wp:query-no-results -->\n' + para('Programs for this directorate will be listed here soon.') + '\n<!-- /wp:query-no-results --></div>\n<!-- /wp:query -->')
    return band(section_title('Directorate', title) + '\n\n' + para(blurb, align='center') + '\n\n' + q, None, 'ncah-directorate-' + slug)
write('programs.html', [page_head('Programs', U + '2023/07/IMG-20230730-WA0012.webp'),
    band(para('Our programs are organised by directorate. Each program shows whether it is running now or proposed for a future year.', align='center'), 'mist', 'ncah-programs-intro', '800px'),
    dsec('youth-sports', 'Youth and Sports Directorate', 'Youth development programs that use culturally relevant physical activity and mentorship, including the Golden Eagles of Hamilton.'),
    dsec('social', 'Social Directorate', 'Community celebrations and food support that build connection, multicultural awareness and integration in Hamilton and surrounding areas.')])

# ---------- Gallery (all videos) ----------
from build_home_vids import VIDS
gg = ('<!-- wp:group {"layout":{"type":"grid","columnCount":3}} -->\n<div class="wp-block-group">' + '\n\n'.join(youtube(u, t) for t, u in VIDS) + '</div>\n<!-- /wp:group -->')
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
