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
a = [page_head('About us', U + '2026/05/About-us-scaled.webp')]
a.append(band(split(U + '2023/12/About-the-Association.webp', 'Who we are', 'The Association',
    'The Nigerian Canadian Association, Hamilton and Environs (NCAH) is a non-profit organization founded in 1999. We support youth to embrace their heritage, pursue academic success and develop their creativity.'),
    None, 'ncah-about-association'))
a.append(band(split(U + '2023/12/The-Nigerian-Spirit-1.webp', 'Why we exist', 'Our Mission',
    'Our mission is to promote unity and provide a conducive environment for individuals with Nigerian heritage to thrive in the community.', True),
    'mist', 'ncah-about-mission'))
goals = ['Enrich Canadian culture with Nigerian traditions.',
         'Be a welcoming hub for diverse social interaction.',
         'Connect children of Nigerian heritage, and others, to their cultural roots.',
         'Provide essential support to members in need.',
         'Enhance the social and economic well-being of members and the community.']
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
a.append(band(split(U + '2026/02/NCAH-Contsitution-and-Bye-law.webp', 'Governance', 'Constitution and By-Laws',
    'Our governing documents set out how the Association is run. Download the signed Constitution and By-Laws.', False,
    buttons([button('Download', U + '2026/02/NCA-Hamilton-Bylaws-Signed.pdf', True)], center=False)), 'mist', 'ncah-foundations'))
write('about-us.html', a)

# ---------- Membership ----------
m = [page_head('Membership', U + '2024/01/Google-Form-Header.webp')]
elig = ('Membership is voluntary and open to all peoples of Nigeria by birth, naturalization, marriage or heritage, '
        'and to others committed to the principles of the Association. We welcome members from Hamilton-Wentworth, Burlington, Oakville, '
        'Kitchener, Waterloo, Guelph, Grimsby and St. Catherine.')
img = f'<!-- wp:image {{"sizeSlug":"large","className":"is-style-rounded"}} -->\n<figure class="wp-block-image size-large is-style-rounded"><img src="{U}2023/12/hi-res-be6cc83762096029bbf781b08a079cb8_crop_north-scaled.webp" alt="NCAH members"/></figure>\n<!-- /wp:image -->'
m.append(band(split(U + '2023/12/hi-res-be6cc83762096029bbf781b08a079cb8_crop_north-scaled.webp', 'Join us', 'Become a Member of the NCAH', elig), None, 'ncah-member-intro'))
form = ('<!-- wp:html -->\n<iframe class="ncah-member-form" src="https://docs.google.com/forms/d/e/1FAIpQLSeCcYE7jPMkRaztM0MxiUieotiyU1Oh0TlIDQP8QM7y4osOgw/viewform?embedded=true" '
        'width="100%" height="800" frameborder="0" marginheight="0" marginwidth="0" title="NCAH membership form" loading="lazy">Loading…</iframe>\n<!-- /wp:html -->')
m.append(band(section_title('Membership form', 'Apply online') + '\n\n' + form, 'mist', 'ncah-member-form-band', '800px'))
write('membership.html', m)

# ---------- Events ----------
q = ('<!-- wp:query {"query":{"perPage":9,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","inherit":false},"className":"ncah-events"} -->\n'
     '<div class="wp-block-query ncah-events"><!-- wp:post-template {"layout":{"type":"grid","columnCount":3}} -->\n'
     '<!-- wp:post-featured-image {"isLink":true,"aspectRatio":"4/3"} /-->\n\n<!-- wp:post-date {"fontSize":"small"} /-->\n\n'
     '<!-- wp:post-title {"level":3,"isLink":true,"fontSize":"medium"} /-->\n\n<!-- wp:post-excerpt {"excerptLength":20} /-->\n<!-- /wp:post-template -->\n\n'
     '<!-- wp:query-pagination {"layout":{"type":"flex","justifyContent":"center"}} -->\n<!-- wp:query-pagination-previous /-->\n\n<!-- wp:query-pagination-numbers /-->\n\n<!-- wp:query-pagination-next /-->\n<!-- /wp:query-pagination -->'
     '</div>\n<!-- /wp:query -->')
write('events.html', [page_head('Events', U + '2023/07/IMG-20230730-WA0012.webp'), band(q, None, 'ncah-events-band')])

# ---------- Contact Us ----------
c = [page_head('Contact Us', U + '2024/01/contact-us.webp')]
c.append(band(section_title('Contact us', 'Get in touch') + '\n\n' +
              para('Get in touch to learn more about our community, membership, and upcoming events.', align='center'), None, 'ncah-contact-intro', '800px'))
info = (heading('Contact', 3, '', None, 'medium', 'ncah-green') + '\n\n' +
        para('Phone: <a href="tel:+12892442568">+1 (289) 244-2568</a>', raw=True) + '\n\n' +
        para('Email: <a href="mailto:info@ncahamilton.ca">info@ncahamilton.ca</a>', raw=True) + '\n\n' +
        heading('Follow us', 3, '', None, 'medium', 'ncah-green') + '\n\n' +
        para('<a href="https://www.facebook.com/NCAHamilton">Facebook</a> · <a href="https://www.instagram.com/ncahamilton/">Instagram</a> · <a href="https://www.youtube.com/@NCAHamilton">YouTube</a>', raw=True))
mapb = ('<!-- wp:html -->\n<iframe title="Map of Hamilton, Ontario" src="https://maps.google.com/maps?q=Hamilton%2C%20Ontario&amp;output=embed" '
        'width="100%" height="320" style="border:0;border-radius:12px" loading="lazy"></iframe>\n<!-- /wp:html -->')
c.append(band(columns([column('<!-- wp:group {"className":"ncah-infocard","layout":{"type":"default"}} -->\n<div class="wp-block-group ncah-infocard">' + info + '</div>\n<!-- /wp:group -->', '40%'), column(heading('Find Us', 3, '', None, 'medium', 'ncah-green') + '\n\n' + mapb, '60%')]), 'mist', 'ncah-contact-info'))
formph = '<!-- wp:shortcode -->\n[wpforms id="810"]\n<!-- /wp:shortcode -->'
c.append(band(section_title('Write to us', 'Send us a message') + '\n\n' + formph, None, 'ncah-contact-form', '800px'))
write('contact-us.html', c)

# ---------- Donate ----------
d = [page_head('Donate', U + '2024/01/contact-us.webp'),
     band(section_title('Give', 'Support NCAH') + '\n\n' +
          para('Your gift supports our community programs and the Youth and Sports Directorate. [Confirm donation page wording and receipting statement before publishing. The form shown is the campaign set in Settings > Zeffy.]') + '\n\n' +
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
    dsec('youth-sports', 'Youth and Sports Directorate', '[Confirm directorate description before publishing.]'),
    dsec('social', 'Social Directorate', '[Confirm directorate description before publishing.]')])

# ---------- Gallery (all videos) ----------
from build_home_vids import VIDS
gg = ('<!-- wp:group {"layout":{"type":"grid","columnCount":3}} -->\n<div class="wp-block-group">' + '\n\n'.join(youtube(u, t) for t, u in VIDS) + '</div>\n<!-- /wp:group -->')
write('gallery.html', [page_head('Gallery', U + '2023/07/IMG-20230730-WA0012.webp'), band(section_title('Watch', 'NCAH videos') + '\n\n' + gg, None, 'ncah-gallery')])
