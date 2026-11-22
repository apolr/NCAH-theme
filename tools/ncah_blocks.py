"""Shared block-markup helpers for the NCAH page builders (build_home.py, build_pages.py)."""
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


def page_head(title, img, eyebrow='Nigerian Canadian Association, Hamilton and Environs'):
    """ncabc-style page title: full-width photo, dark overlay, centred serif H1 with a short red rule."""
    a = {'url': img, 'dimRatio': 55, 'align': 'full', 'minHeight': 380, 'contentPosition': 'center center', 'className': 'ncah-page-head'}
    return (f'<!-- wp:cover {j(a)} -->\n<div class="wp-block-cover alignfull ncah-page-head" style="min-height:380px">'
            f'<span aria-hidden="true" class="wp-block-cover__background has-background-dim-60 has-background-dim"></span>'
            f'<img class="wp-block-cover__image-background" alt="" src="{img}" data-object-fit="cover"/>'
            f'<div class="wp-block-cover__inner-container">' + para(eyebrow, 'ncah-eyebrow', 'center', None, 'white') + '\n\n' + heading(title, 1, '', 'center', 'hero', 'white') + '</div></div>\n<!-- /wp:cover -->')

def split(img, eyebrow, title, text, reverse=False, extra=''):
    """Square image beside text, as in the ncabc.org content blocks."""
    im = f'<!-- wp:image {{"sizeSlug":"large","className":"ncah-split-img"}} -->\n<figure class="wp-block-image size-large ncah-split-img"><img src="{img}" alt="{html.escape(title)}"/></figure>\n<!-- /wp:image -->'
    tx = (para(eyebrow, 'ncah-eyebrow', None, None, 'ncah-red') + '\n\n' + heading(title, 2, '', None, 'x-large') + '\n\n' + para(text) + (('\n\n' + extra) if extra else ''))
    cols = [column(im, '50%'), column(tx, '50%')]
    if reverse: cols = cols[::-1]
    a = {'verticalAlignment': 'center', 'className': 'ncah-split'}
    return ('<!-- wp:columns {"verticalAlignment":"center","className":"ncah-split"} -->\n<div class="wp-block-columns are-vertically-aligned-center ncah-split">'
            + '\n\n'.join(cols).replace('<!-- wp:column {"width":"50%"} -->', '<!-- wp:column {"verticalAlignment":"center","width":"50%"} -->').replace('<div class="wp-block-column" style', '<div class="wp-block-column is-vertically-aligned-center" style')
            + '</div>\n<!-- /wp:columns -->')

def section_title(eyebrow, title, center=True):
    al = 'center' if center else None
    return para(eyebrow, 'ncah-eyebrow', al, None, 'ncah-red') + '\n\n' + heading(title, 2, '', al, 'x-large')

def write(name, blocks):
    p = pathlib.Path(__file__).resolve().parent.parent / 'content' / name
    p.write_text('\n\n'.join(blocks) + '\n')
    print('wrote', p.name, len('\n\n'.join(blocks)), 'bytes')
