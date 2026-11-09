# v11: users + new main API + logo + light/dark mode + new login/sign-up pages
from templates_ui2 import TEMPLATES as _T, _P, ic, CSS2, LGHEAD, LGFOOT

_P.update({
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "image": '<rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21"/>',
    "userplus": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" x2="19" y1="8" y2="14"/><line x1="22" x2="16" y1="11" y2="11"/>',
})

T = dict(_T)


def sub(key, old, new, count=1):
    assert old in T[key], "patch target missing in %s: %s" % (key, old[:70])
    T[key] = T[key].replace(old, new, count)


# ================================================================ light / dark mode
MODE_CSS = r"""
.brandimg{width:100%;height:100%;object-fit:cover;border-radius:inherit;display:block}
.tile:has(.brandimg),.logo-t:has(.brandimg){overflow:hidden;padding:0}
.modefloat{position:fixed;top:14px;right:14px;z-index:60}
html[data-mode=light]{color-scheme:light;--bg:#eef2f9;--card:rgba(255,255,255,.93);--bd:rgba(var(--acrgb),.32);--tx:#0f1a2e;--mu:#5a6a85;--gl:0 0 18px rgba(var(--acrgb),.25)}
html[data-mode=light] body{background-image:radial-gradient(60% 50% at 15% 0%,rgba(var(--acrgb),.13),transparent 70%),radial-gradient(50% 45% at 100% 20%,rgba(var(--ac2rgb),.11),transparent 70%),linear-gradient(rgba(0,0,0,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.03) 1px,transparent 1px)}
html[data-mode=light] body::before,html[data-mode=light] body::after{opacity:.12}
html[data-mode=light] h2{background:linear-gradient(90deg,#0f1a2e,var(--ac) 70%,var(--ac2));-webkit-background-clip:text;background-clip:text;color:transparent}
html[data-mode=light] .stat b{background:linear-gradient(90deg,#0f1a2e,var(--ac));-webkit-background-clip:text;background-clip:text;color:transparent}
html[data-mode=light] .card,html[data-mode=light] .stat,html[data-mode=light] .kpi,html[data-mode=light] .klist,html[data-mode=light] .gcard,html[data-mode=light] .nt{box-shadow:0 6px 22px rgba(30,50,90,.10)}
html[data-mode=light] input,html[data-mode=light] select,html[data-mode=light] textarea{background:#fff;border-color:rgba(var(--acrgb),.35);color:var(--tx)}
html[data-mode=light] button.o{color:var(--tx)}
html[data-mode=light] .top,html[data-mode=light] .atop,html[data-mode=light] .nav{background:rgba(255,255,255,.88)}
html[data-mode=light] .side{background:rgba(255,255,255,.98);box-shadow:12px 0 40px rgba(30,50,90,.18)}
html[data-mode=light] .adr{background:#fff;box-shadow:0 0 50px rgba(30,50,90,.2)}
html[data-mode=light] .adr .ax{color:var(--tx)}
html[data-mode=light] .adr a.on{color:#fff}
html[data-mode=light] .aburger i{background:var(--ac)}
html[data-mode=light] .player{background:rgba(var(--acrgb),.08)}
html[data-mode=light] pre,html[data-mode=light] code{background:rgba(var(--acrgb),.08);color:var(--acd)}
html[data-mode=light] .gb select,html[data-mode=light] .gb .qi{background:#fff}
html[data-mode=light] .tbl th{background:#e6ecf7}
html[data-mode=light] .modal .bx{background:#fff}
html[data-mode=light] .logo{background:linear-gradient(90deg,var(--ac),var(--ac2));-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none}
html[data-mode=light] .ic,html[data-mode=light] .iconbtn,html[data-mode=light] .iconbtn .ic,html[data-mode=light] .tile .ic,html[data-mode=light] .side a .ic,html[data-mode=light] .cp,html[data-mode=light] .player button .ic{color:var(--ac)}
html[data-mode=light] .welcome .tile .ic,html[data-mode=light] .btn .ic,html[data-mode=light] button .ic,html[data-mode=light] .lg .go .ic,html[data-mode=light] .player #pp .ic{color:#fff}
html[data-mode=light] .gen .ic{color:var(--ac)}
html[data-mode=light] .wrap a:not(.btn):not(.pill){color:var(--ac)}
html[data-mode=light] .src,html[data-mode=light] .tbl td code,html[data-mode=light] .gs,html[data-mode=light] .cd{color:var(--acd)}
html[data-mode=light] .pill.a{color:#047857}html[data-mode=light] .pill.e{color:#be123c}html[data-mode=light] .pill.p{color:var(--acd)}html[data-mode=light] .pill.c{color:#0e7490}
html[data-mode=light] .lg .box{background:rgba(255,255,255,.92)}
html[data-mode=light] .lg .fld{background:#fff}
html[data-mode=light] .lg .tag,html[data-mode=light] .lg .sess{color:var(--ac)}
html[data-mode=light] .lg .fld .ic,html[data-mode=light] .lg .eye{color:#64748b}
html[data-mode=light] .krow .m code,html[data-mode=light] .krow .d{color:var(--mu)}
html[data-mode=light] .amt{color:var(--tx)}html[data-mode=light] .amt.on{color:#fff}
"""

MODE_JS = r"""
(function(){var D='{{site_mode|default("dark")}}',de=document.documentElement;
function saved(){try{return localStorage.rgmode}catch(e){return null}}
function apply(m){de.setAttribute('data-mode',m);var t=document.querySelector('meta[name=theme-color]');if(t)t.setAttribute('content',m==='light'?'#eef2f9':'#04040a')}
apply(saved()||D);
var SUN='<svg class="ic" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>',
MOON='<svg class="ic" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>';
function paint(){var b=document.getElementById('modeBtn');if(b)b.innerHTML=de.getAttribute('data-mode')==='light'?MOON:SUN}
document.addEventListener('DOMContentLoaded',function(){var host=document.querySelector('.top')||document.querySelector('.atop'),b=document.createElement('button');
b.id='modeBtn';b.type='button';b.setAttribute('aria-label','Switch light / dark mode');b.title='Light / Dark';
if(host){b.className='iconbtn';if(host.classList.contains('atop'))b.style.marginLeft='auto';host.appendChild(b)}else{b.className='iconbtn modefloat';document.body.appendChild(b)}
b.onclick=function(){var m=de.getAttribute('data-mode')==='light'?'dark':'light';try{localStorage.rgmode=m}catch(e){}apply(m);paint()};paint()});
})();
"""

for k in T:
    if CSS2 in T[k]:
        T[k] = T[k].replace(CSS2, CSS2 + MODE_CSS)
    if "</head>" in T[k]:
        T[k] = T[k].replace("</head>", "<script>" + MODE_JS + "</script></head>", 1)

# ================================================================ reseller / user sidebar
sub("rbase.html", "<span class=tile>{{ic('crown',22)}}</span><div><b class=logo>{{BRAND}}</b><div class=mu>{{r.username}}</div></div>",
    "<span class=tile>{{brand_mark('crown',22)}}</span><div><b class=logo>{{BRAND}}</b><div class=mu>{{r.username}} &middot; {{'User' if r.role=='user' else 'Reseller'}}</div></div>")
sub("rbase.html", """<a href="/bot-make" class="{{'on' if page=='botmake'}}">{{ic('bot')}} Bot Make</a>
<a href="/security" class="{{'on' if page=='security'}}">{{ic('shield2')}} Security</a>""",
    """{% if r.role!='user' %}<a href="/bot-make" class="{{'on' if page=='botmake'}}">{{ic('bot')}} Bot Make</a>
<a href="/security" class="{{'on' if page=='security'}}">{{ic('shield2')}} Security</a>{% endif %}""")
sub("rbase.html", """<a href="/api-docs" class="{{'on' if page=='api'}}">{{ic('code')}} API &amp; Docs</a>""",
    """{% if r.role!='user' %}<a href="/api-docs" class="{{'on' if page=='api'}}">{{ic('code')}} API &amp; Docs</a>{% endif %}""")
sub("dashboard.html", "<span class=\"tile\">{{ic('crown',28)}}</span>", "<span class=\"tile\">{{brand_mark('crown',28)}}</span>")
sub("settings.html", "(Even with the password, a new device still needs admin approval.)",
    "{% if r.role!='user' %}(Even with the password, a new device still needs admin approval.){% endif %}")
sub("settings.html", """<label class=mu style="display:flex;gap:8px;align-items:center"><input type=checkbox name=newkey value=1 style="width:auto"> Also generate a new API key (old API key stops working)</label>""",
    """{% if r.role!='user' %}<label class=mu style="display:flex;gap:8px;align-items:center"><input type=checkbox name=newkey value=1 style="width:auto"> Also generate a new API key (old API key stops working)</label>{% endif %}""")

# ================================================================ login + sign-up pages
AUTH_CSS = r"""<style>
.lg{position:relative;overflow:hidden}
.lg::before,.lg::after{content:"";position:fixed;width:420px;height:420px;border-radius:50%;filter:blur(120px);opacity:.35;z-index:-1;pointer-events:none}
.lg::before{background:var(--ac);left:-120px;top:-100px}.lg::after{background:var(--ac2);right:-120px;bottom:-100px}
.lg .box{position:relative;border:0;padding:30px 24px 24px;background:rgba(10,14,30,.82);animation:rise .6s ease both}
.lg .box::before{content:"";position:absolute;inset:0;border-radius:inherit;padding:1.6px;background:linear-gradient(135deg,var(--ac),transparent 40%,var(--ac2) 75%,var(--ac));-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@keyframes ring{0%{box-shadow:0 0 0 0 rgba(var(--acrgb),.55)}100%{box-shadow:0 0 0 22px rgba(var(--acrgb),0)}}
.lg .logo-t{width:76px;height:76px;border-radius:24px;animation:ring 2.4s ease-out infinite}
.lg h1{background:linear-gradient(90deg,var(--tx),var(--acl) 60%,var(--acl2));-webkit-background-clip:text;background-clip:text;color:transparent;letter-spacing:.04em}
.lg .sub{text-align:center;color:var(--mu);margin:6px 0 0;font-size:14px}
.lg .go{margin-top:20px;position:relative;overflow:hidden;cursor:pointer}
.lg .go::after{content:"";position:absolute;top:0;left:-60%;width:40%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent);transform:skewX(-20deg);animation:shine 3.2s ease-in-out infinite}
@keyframes shine{0%,60%{left:-60%}100%{left:130%}}
.lg .or{display:flex;align-items:center;gap:12px;margin:20px 0 14px;color:var(--mu);font-size:12px;font-weight:700;letter-spacing:.2em}
.lg .or i{flex:1;height:1px;background:linear-gradient(90deg,transparent,var(--bd),transparent)}
.lg .mk{display:flex;align-items:center;justify-content:center;gap:10px;width:100%;padding:13px;border-radius:14px;font-weight:800;font-size:14px;letter-spacing:.08em;color:var(--tx);background:rgba(var(--acrgb),.08);border:1.5px solid var(--bd);transition:.2s}
.lg .mk:hover{background:rgba(var(--acrgb),.18);border-color:var(--ac);transform:translateY(-1px)}
.lg .mk .ic{color:var(--ac);margin:0}
.lg .hint2{font-size:12px;color:var(--mu);margin:6px 2px 0}
.lg .fld.bad{border-color:var(--er)!important}
.lg .back{display:block;text-align:center;margin-top:16px;font-size:14px;color:var(--mu)}.lg .back b{color:var(--ac2)}
html[data-mode=light] .lg .box{background:rgba(255,255,255,.94)}
html[data-mode=light] .lg .back b{color:var(--ac)}
</style>"""

EYE_JS = """<script>try{['mu','mt','mp','ts'].forEach(function(k){sessionStorage.removeItem(k)})}catch(e){}
const EI='{{ic('eye',20)|e}}',EO='{{ic('eyeoff',20)|e}}';
document.querySelectorAll('.eye').forEach(function(b){b.onclick=function(){var i=document.getElementById(b.dataset.t),h=i.type==='password';i.type=h?'text':'password';b.innerHTML=h?EO:EI}});</script>"""

T["login.html"] = LGHEAD + AUTH_CSS + """
<div class="logo-t">{{brand_mark('key',34)}}</div><h1>{{BRAND}}</h1><p class="sub">Welcome back &mdash; sign in to continue</p>
<div class="dv"><i></i><u></u><i></i></div>
{% with m=get_flashed_messages(with_categories=true) %}{% for c,t in m %}<div class="flash {{c}}">{{t}}</div>{% endfor %}{% endwith %}
<form method=post action="{{action}}" autocomplete=on>
<label for=u>Username</label><div class="fld">{{ic('user',20)}}<input id=u name=username value="{{u or ''}}" placeholder="Enter your username" required {{'' if u else 'autofocus'}} autocomplete=username autocapitalize=off></div>
<label for=pw>Password</label><div class="fld">{{ic('lock',20)}}<input id=pw name=password type=password placeholder="Enter your password" required {{'autofocus' if u}} autocomplete=current-password><button type=button class=eye data-t=pw aria-label="Show password">{{ic('eye',20)}}</button></div>
<button class="go">LOGIN {{ic('arrow',20)}}</button></form>
{% if signup %}<div class="or"><i></i>OR<i></i></div><a class="mk" href="/signup">{{ic('userplus',20)}} CREATE NEW ACCOUNT</a>{% endif %}
""" + LGFOOT + EYE_JS + "</body></html>"

T["signup.html"] = LGHEAD + AUTH_CSS + """
<div class="logo-t">{{brand_mark('userplus',34)}}</div><h1>Create Account</h1><p class="sub">Join {{BRAND}} in a few seconds</p>
<div class="dv"><i></i><u></u><i></i></div>
{% with m=get_flashed_messages(with_categories=true) %}{% for c,t in m %}<div class="flash {{c}}">{{t}}</div>{% endfor %}{% endwith %}
<form method=post action="/signup" autocomplete=off id=sf>
<label for=u>Username</label><div class="fld">{{ic('user',20)}}<input id=u name=username value="{{u or ''}}" placeholder="Choose a username" required minlength=3 maxlength=24 pattern="[A-Za-z0-9_.\\-]{3,24}" autofocus autocomplete=username autocapitalize=off></div>
<div class="hint2">3-24 characters: letters, numbers, _ . -</div>
<label for=pw>Password</label><div class="fld">{{ic('lock',20)}}<input id=pw name=password type=password placeholder="Create a password (min 6)" required minlength=6 autocomplete=new-password><button type=button class=eye data-t=pw aria-label="Show password">{{ic('eye',20)}}</button></div>
<label for=cf>Confirm password</label><div class="fld" id=cfb>{{ic('lock',20)}}<input id=cf name=confirm type=password placeholder="Type the password again" required minlength=6 autocomplete=new-password><button type=button class=eye data-t=cf aria-label="Show password">{{ic('eye',20)}}</button></div>
<button class="go">CREATE ACCOUNT {{ic('arrow',20)}}</button></form>
<a class="back" href="/login">Already have an account? <b>Login</b></a>
""" + LGFOOT + EYE_JS + """<script>const P=document.getElementById('pw'),C=document.getElementById('cf'),B=document.getElementById('cfb');
function chk(){B.classList.toggle('bad',C.value.length>0&&C.value!==P.value)}P.oninput=C.oninput=chk;
document.getElementById('sf').onsubmit=function(e){if(P.value!==C.value){e.preventDefault();B.classList.add('bad');C.focus()}};</script></body></html>"""

for k in ("login.html", "signup.html"):         # these were built after the loop above -> add mode script now
    T[k] = T[k].replace("</head>", "<script>" + MODE_JS + "</script></head>", 1) if MODE_JS not in T[k] else T[k]
    T[k] = T[k].replace(CSS2, CSS2 + MODE_CSS) if MODE_CSS not in T[k] else T[k]

# ================================================================ admin: menu, resellers/users, products
sub("abase.html", '<a href="/admin/backup"', '<a href="/admin/branding" class="{{\'on\' if page==\'branding\'}}">Logo &amp; Theme</a><a href="/admin/backup"')
sub("abase.html", "{{ic('tool')}} ADMIN", "<span style=\"width:22px;height:22px;display:inline-flex\">{{brand_mark('tool',22)}}</span> ADMIN")
sub("abase.html", "<a href=\"/admin/resellers\" class=\"{{'on' if page=='resellers'}}\">Resellers</a>",
    "<a href=\"/admin/resellers\" class=\"{{'on' if page=='resellers'}}\">Resellers</a><a href=\"/admin/resellers?role=user\" class=\"{{'on' if page=='resellers' and request.args.get('role')=='user'}}\">Users</a>")

T["admin_resellers.html"] = r"""{% extends 'abase.html' %}{% block c %}<h2>Resellers &amp; Users</h2>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 4px">
<a class=btn href="/admin/resellers" style="{{'' if show=='reseller' else 'background:transparent;border:1px solid var(--bd);box-shadow:none'}}">Resellers <span class="pill c">{{cnt.get('reseller',0)}}</span></a>
<a class=btn href="/admin/resellers?role=user" style="{{'' if show=='user' else 'background:transparent;border:1px solid var(--bd);box-shadow:none'}}">Users <span class="pill c">{{cnt.get('user',0)}}</span></a></div>
<div class=card><h3>Create account</h3><form class=row method=post><input name=username placeholder="Username" required><input name=password placeholder="Password" required>
<select name=role style="width:120px"><option value=reseller {{'selected' if show=='reseller'}}>Reseller</option><option value=user {{'selected' if show=='user'}}>User</option></select>
<input name=credit type=number step=any value=0 placeholder="Starting credit" style="width:140px"><input name=tg_chat placeholder="Telegram Chat ID (resellers, optional)" inputmode=numeric style="width:230px"><button>Create</button></form>
<p class=hint>Users can also sign up themselves from the login page (Create New Account). Users see the USER price, resellers the RESELLER price.</p></div>
<div class="card tw"><table><tr><th>{{'User' if show=='user' else 'Reseller'}}</th><th>Balance</th><th>Keys</th>{% if show!='user' %}<th>Telegram</th>{% endif %}<th>Status</th><th></th></tr>
{% for x in rows %}<tr><td>{{x.username}}</td><td>{{x.balance|cur}}</td><td>{{x.kc}}</td>{% if show!='user' %}<td>{% if x.tg_chat %}<span class="pill a">Linked</span> <span class=mu>{{x.tg_chat}}</span>{% else %}<span class="pill e">Not linked</span><form class=row method=post action="/admin/reseller/{{x.id}}" style="margin-top:6px;flex-wrap:nowrap"><input type=hidden name=action value=tg><input name=tg_chat list=seenids placeholder="Chat ID" inputmode=numeric style="width:130px"><button class=g>Link</button></form>{% endif %}</td>{% endif %}<td>{% if x.active %}<span class="pill a">Active</span>{% else %}<span class="pill e">Disabled</span>{% endif %}</td>
<td><a class=btn href="/admin/reseller/{{x.id}}">Manage</a></td></tr>{% else %}<tr><td colspan=6>None yet</td></tr>{% endfor %}</table></div>
{% if show!='user' %}<datalist id=seenids>{% for s in seen %}<option value="{{s.chat_id}}">{{s.name}} {{s.username}}</option>{% endfor %}</datalist>{% if seen %}<div class=card><h3>Pressed /start in the bot (not linked yet)</h3>{% for s in seen %}<span class="pill p" style="margin:2px">{{s.name or "?"}}{% if s.username %} @{{s.username}}{% endif %} &middot; {{s.chat_id}}</span>{% endfor %}<p class=hint>Type or pick the Chat ID in the reseller row above and press Link. A test message is sent to confirm.</p></div>{% endif %}{% endif %}{% endblock %}"""

# admin_reseller: hide reseller-only cards for users
sub("admin_reseller.html", '<div class=card><h3>{{ic(\'send\',20)}} Telegram &amp; Security</h3>', "{% if r.role!='user' %}<div class=card><h3>{{ic('send',20)}} Telegram &amp; Security</h3>")
sub("admin_reseller.html", '<div class=card><h3>Change Password</h3>', "{% endif %}<div class=card><h3>Change Password</h3>")
sub("admin_reseller.html", '<div class=card><h3>Custom Prices</h3>', "{% if r.role!='user' %}<div class=card><h3>Custom Prices</h3>")
sub("admin_reseller.html", "<button class=g style=\"margin-top:10px\">Save Prices</button></form></div>",
    "<button class=g style=\"margin-top:10px\">Save Prices</button></form></div>{% else %}<div class=card><h3>Price</h3><p class=mu>This is a <b>User</b> account: it always pays the USER price of each plan (set in Products).</p></div>{% endif %}")
sub("admin_reseller.html", "<h2>{{r.username}} <span class=mu>", "<h2>{{r.username}} <span class=\"pill {{'c' if r.role=='user' else 'p'}}\">{{'USER' if r.role=='user' else 'RESELLER'}}</span> <span class=mu>")

# admin products: user price column + old API marker
sub("admin_products.html", "<th>ID</th><th>Time</th><th>Price</th>", "<th>ID</th><th>Time</th><th>Reseller price</th><th>User price</th>")
sub("admin_products.html", """<td><input name=price type=number step=any value="{{pl.price}}" style="width:90px"></td>""",
    """<td><input name=price type=number step=any value="{{pl.price}}" style="width:90px"></td><td><input name=user_price type=number step=any value="{{user_price_of(pl)}}" style="width:90px"></td>""")
sub("admin_products.html", """<input name=price type=number step=any min=0 placeholder="Price" required style="width:120px">""",
    """<input name=price type=number step=any min=0 placeholder="Reseller price" required style="width:130px"><input name=user_price type=number step=any min=0 placeholder="User price (auto)" style="width:140px">""")
sub("admin_products.html", """{% elif pl.mode=='provider' %}<span class="pill c">Main API #{{pl.prov_pid}}</span>{% endif %}""",
    """{% elif pl.mode=='provider' %}{% if pl.prov_src=='v2' %}<span class="pill c">Main API #{{pl.prov_pid}}</span>{% else %}<span class="pill e">Old API - delete</span>{% endif %}{% endif %}""")
sub("admin_products.html", "<tr><td colspan=5>No plans</td></tr>", "<tr><td colspan=6>No plans</td></tr>")

# ================================================================ admin: Main API (new) + logo page
TABS = """<div style="display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 4px">
<a class=btn href="/admin/main-api" style="{{'' if page2=='c' else 'background:transparent;border:1px solid var(--bd);box-shadow:none'}}">{{ic('key',16)}}Connection</a>
<a class=btn href="/admin/main-api/products" style="{{'' if page2=='p' else 'background:transparent;border:1px solid var(--bd);box-shadow:none'}}">{{ic('box',16)}}All Products</a></div>"""

T["admin_mapi.html"] = """{% extends 'abase.html' %}{% block c %}{% set page2='c' %}<h2>{{ic('code',24)}} Main API</h2>""" + TABS + """
<div class=card><h3>{{ic('key',20)}} Connect</h3>
<p class=mu>Enter the server URL and the API token of your account on the main panel. Connect works with the token only.</p>
<form method=post><input type=hidden name=action value=save>
<p class=mu>Server URL</p><input name=base value="{{base}}" style="width:100%" required placeholder="https://official-seller-4.onrender.com">
<p class=mu>API Token{% if tail %} &mdash; saved (ends with <code>{{tail}}</code>). Leave empty to keep it.{% endif %}</p>
<input name=token type=password autocomplete=off placeholder="Paste your API token" style="width:100%" {{'' if tail else 'required'}}>
<button class=g style="margin-top:12px">{{ic('check')}} Save &amp; Connect</button></form></div>
<div class=card><h3>{{ic('wallet',20)}} Status &amp; Balance</h3>
{% if st %}{% if st.ok %}<span class="pill a">Connect successful</span>
<div class=mu style="margin-top:8px">Account: <b>{{st.username}}</b></div>
<div style="font-size:30px;font-weight:800;color:#34d399;margin:4px 0">{{st.balance|cur}}</div>
{% else %}<span class="pill e">Not connected</span><div class=mu style="margin:8px 0">{{st.msg}}</div>{% endif %}
<div class=mu>Last checked: {{st.ts|dt}}</div>
{% else %}<div class=mu>Not checked yet. Save your token to connect.</div>{% endif %}
<form method=post style="margin-top:12px"><input type=hidden name=action value=check><button>{{ic('wallet')}} Check connection &amp; balance</button></form></div>
{% if st and st.ok %}<a class=btn href="/admin/main-api/products">{{ic('box',16)}} Open All Products &rarr;</a>{% endif %}
{% endblock %}"""

T["admin_mapi_products.html"] = """{% extends 'abase.html' %}{% block c %}{% set page2='p' %}<h2>{{ic('box',24)}} All Products</h2>""" + TABS + """
{% if not cat %}<div class=card>No products yet. Connect the API first (Connection tab), then press Refresh.<br><br><a class=btn href="/admin/main-api/products?refresh=1">Refresh from API</a></div>
{% else %}
<form method=post>
<div class=card><div class=mu>Tick the products (or single plans) you want to sell, then press <b>Import selected</b>. Buying is done live from the main API.</div>
<div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:12px">
<label class=mu>Reseller price = cost + <input name=mk_res id=mkr type=number step=any min=0 value="{{mr|money}}" style="width:80px"> %</label>
<label class=mu>User price = cost + <input name=mk_user id=mku type=number step=any min=0 value="{{mu|money}}" style="width:80px"> %</label></div>
<label class=mu style="display:block;margin-top:10px"><input type=checkbox name=overwrite> Also reset the prices of plans that are already imported</label>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px">
<button class=g name=scope value=sel>{{ic('plus')}} Import selected</button>
<button name=scope value=all onclick="return confirm('Import ALL products from the main API?')">{{ic('box')}} Import ALL</button>
<button type=submit name=scope value=sync class=o onclick="return confirm('Re-price every imported plan with fresh costs and these percentages?')">Sync prices</button>
<a class=btn href="/admin/main-api/products?refresh=1" style="background:transparent;border:1px solid var(--bd);box-shadow:none">Refresh</a>
<label class=mu style="margin-left:auto;display:flex;align-items:center;gap:6px"><input type=checkbox id=selall style="width:auto"> Select all</label></div>
<div class=mu style="margin-top:8px">List fetched: {{cat.ts|dt}} &middot; Edit single prices later in <a href="/admin/products">Products</a>.</div></div>
{% for g in groups %}<div class=card><div style="display:flex;justify-content:space-between;align-items:center"><h3>{{g.name}}</h3><label class=mu style="display:flex;align-items:center;gap:6px"><input type=checkbox class=ga style="width:auto"> all</label></div>
<div class=tw><table><tr><th></th><th>Plan</th><th>ID</th><th>Cost</th><th>Reseller</th><th>User</th><th>Status</th></tr>
{% for p in g.plans %}<tr><td><input type=checkbox name=pid value="{{p.pid}}" class=pc style="width:auto"></td><td>{{p.name}}</td><td>{{p.pid}}</td>
<td>{{p.cost|cur}}</td><td class=rp data-c="{{p.cost}}">-</td><td class=up data-c="{{p.cost}}">-</td>
<td>{% if p.mine %}<span class="pill a">Imported</span> <span class=mu>R {{p.mine.price|cur}} / U {{p.mine.user_price|cur}}</span>{% else %}<span class="pill p">New</span>{% endif %}{% if not p.avail %} <span class="pill e">Out</span>{% endif %}</td></tr>{% else %}<tr><td colspan=7 class=mu>No plans</td></tr>{% endfor %}</table></div></div>
{% else %}<div class=card>The product list is empty.</div>{% endfor %}
</form>
<script>
const f2=v=>{v=Math.round(v*100)/100;return '{{CURRENCY}}'+v},mkr=document.getElementById('mkr'),mku=document.getElementById('mku');
function calc(){const a=parseFloat(mkr.value)||0,b=parseFloat(mku.value)||0;document.querySelectorAll('.rp').forEach(e=>e.textContent=f2(e.dataset.c*(1+a/100)));document.querySelectorAll('.up').forEach(e=>e.textContent=f2(e.dataset.c*(1+b/100)))}
mkr.oninput=mku.oninput=calc;calc();
document.querySelectorAll('.ga').forEach(g=>g.onchange=()=>g.closest('.card').querySelectorAll('.pc').forEach(c=>c.checked=g.checked));
document.getElementById('selall').onchange=function(){document.querySelectorAll('.pc,.ga').forEach(c=>c.checked=this.checked)};
</script>
{% endif %}{% endblock %}"""

T["admin_branding.html"] = """{% extends 'abase.html' %}{% block c %}<h2>{{ic('image',24)}} Logo &amp; Theme</h2>
<div class=card><h3>{{ic('image',20)}} Logo</h3>
<p class=mu>This picture replaces the small icon at the top of the menu (and on the login page and dashboard). PNG, JPG, WEBP or GIF, up to 8 MB. It is cropped to a square automatically.</p>
<div style="display:flex;align-items:center;gap:16px;margin:12px 0"><span class=tile style="width:84px;height:84px;border-radius:24px;overflow:hidden" id=pv>{{brand_mark('crown',34)}}</span>
<div class=mu>{% if has_logo %}Current logo{% else %}No logo yet - the default icon is shown{% endif %}</div></div>
<form method=post enctype=multipart/form-data><input type=hidden name=action value=logo>
<input type=file name=logo id=lf accept="image/*" required style="width:100%">
<button class=g style="margin-top:12px">{{ic('plus')}} {{'Replace logo' if has_logo else 'Add logo'}}</button></form>
{% if has_logo %}<form method=post style="margin-top:10px" onsubmit="return confirm('Remove the logo?')"><input type=hidden name=action value=remove><button class=r>{{ic('trash',16)}} Remove logo</button></form>{% endif %}</div>
<div class=card><h3>{{ic('palette',20)}} Look &amp; sign-up</h3>
<p class=mu>Everybody can switch Light / Dark with the sun / moon button at the top. This sets what a visitor sees the first time.</p>
<form method=post><input type=hidden name=action value=look>
<p class=mu>Default mode</p><select name=mode style="width:100%"><option value=dark {{'selected' if mode!='light'}}>Dark</option><option value=light {{'selected' if mode=='light'}}>Light (white)</option></select>
<label class=mu style="display:flex;gap:8px;align-items:center;margin-top:12px"><input type=checkbox name=signup value=1 style="width:auto" {{'checked' if signup}}> Allow new users to create an account (Create New Account button)</label>
<button class=g style="margin-top:12px">{{ic('save')}} Save</button></form></div>
<script>document.getElementById('lf').onchange=function(){const f=this.files[0];if(!f)return;const u=URL.createObjectURL(f);document.getElementById('pv').innerHTML='<img class=brandimg src="'+u+'">'}</script>
{% endblock %}"""

TEMPLATES = T
