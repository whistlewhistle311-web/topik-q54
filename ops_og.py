import re,os,glob,html
from playwright.sync_api import sync_playwright
os.chdir('/home/claude/topik-q54')
B='https://whistlewhistle311-web.github.io/topik-q54/'
pages=['index.html','topik-53/index.html','topik-51-52/index.html']+sorted(glob.glob('practice/*/index.html'))+(['practice/index.html'] if os.path.exists('practice/index.html') else [])
T='''<html><head><meta charset="utf-8"><style>body{margin:0;width:1200px;height:630px;background:#14213d;color:#f5f1e8;font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif;position:relative;overflow:hidden}
.k{position:absolute;left:80px;top:80px;font-size:28px;letter-spacing:.18em;color:#f2b880;font-weight:700}
.t{position:absolute;left:80px;top:140px;width:1000px;font-size:64px;line-height:1.18;font-weight:800;word-break:keep-all}
.s{position:absolute;left:80px;bottom:80px;font-size:28px;color:#c9d1e3}
.b{position:absolute;right:-40px;bottom:-60px;font-size:330px;font-weight:900;color:rgba(242,184,128,.12)}</style></head><body>
<div class="b">{big}</div><div class="k">TOPIK II · WRITING</div><div class="t">{title}</div><div class="s">Free guide · model answers · scoring</div></body></html>'''
with sync_playwright() as p:
    br=p.chromium.launch();pg=br.new_page(viewport={'width':1200,'height':630})
    for f in pages:
        s=open(f).read()
        t=html.unescape(re.search(r'<meta property="og:title" content="([^"]*)"',s).group(1))
        t=re.sub(r'\s*\([^)]*[가-힣][^)]*\)\s*$','',t)
        big={'index.html':'54','topik-53/index.html':'53','topik-51-52/index.html':'51'}.get(f,'54')
        slug=('home' if f=='index.html' else f.replace('/index.html','').replace('/','-'))
        pg.set_content(T.replace('{title}',html.escape(t)).replace('{big}',big));pg.wait_for_timeout(200)
        pg.screenshot(path=f'og/{slug}.png')
        s=re.sub(r'<meta property="og:image" content="[^"]*">',f'<meta property="og:image" content="{B}og/{slug}.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',s,count=1)
        open(f,'w').write(s);print(slug,t[:60])
    br.close()
