"""v12 templates: separate Users section, ban / delete / restore, admin first-time setup + admin login code."""
from templates_ui3 import TEMPLATES as T, ic  # noqa: F401


def sub(name, old, new):
    assert old in T[name], (name, old[:70])
    T[name] = T[name].replace(old, new, 1)


# ---- admin menu: Users is its own page now
sub("abase.html",
    "<a href=\"/admin/resellers?role=user\" class=\"{{'on' if page=='resellers' and request.args.get('role')=='user'}}\">Users</a>",
    "<a href=\"/admin/users\" class=\"{{'on' if page=='users'}}\">Users</a>")

# ---- admin home: separate Users counter
sub("admin_home.html", "<div class=stat><span class=mu>Resellers</span><b>{{st.resellers}}</b></div>",
    "<div class=stat><span class=mu>Resellers</span><b>{{st.resellers}}</b></div><div class=stat><span class=mu>Users</span><b>{{st.users}}</b></div>")

# ---- ONE list template for Resellers and for Users
T["admin_accounts.html"] = r"""{% extends 'abase.html' %}{% block c %}<h2>{{'Users' if kind=='user' else 'Resellers'}}</h2>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 4px">
{% for k,l in (('active','Active'),('banned','Banned'),('deleted','Deleted')) %}<a class=btn href="{{base}}?st={{k}}" style="{{'' if st==k else 'background:transparent;border:1px solid var(--bd);box-shadow:none'}}">{{l}} <span class="pill {{'a' if k=='active' else 'e'}}">{{cnt[k]}}</span></a>{% endfor %}</div>
{% if st=='active' %}<div class=card><h3>{{'Create user' if kind=='user' else 'Create reseller'}}</h3><form class=row method=post><input name=username placeholder="Username" required><input name=password placeholder="Password" required>
<input name=credit type=number step=any value=0 placeholder="Starting credit" style="width:140px">
{% if kind!='user' %}<input name=tg_chat placeholder="Telegram Chat ID (optional)" inputmode=numeric style="width:230px"><input type=hidden name=role value=reseller>{% endif %}<button>Create</button></form>
{% if kind=='user' %}<p class=hint>Users can also sign up themselves from the login page. Users see the USER price. They never appear in the Resellers page.</p>{% endif %}</div>{% endif %}
<form class=row method=get action="{{base}}" style="margin:8px 0"><input type=hidden name=st value="{{st}}"><input name=q value="{{sq}}" placeholder="Search username" style="flex:1;min-width:140px"><button>Search</button></form>
<div class="card tw"><table><tr><th>{{'User' if kind=='user' else 'Reseller'}}</th><th>Balance</th><th>Keys</th>{% if kind!='user' %}<th>Telegram</th>{% endif %}<th>Status</th><th></th></tr>
{% for x in rows %}<tr><td>{{x.username}}</td><td>{{x.balance|cur}}</td><td>{{x.kc}}</td>
{% if kind!='user' %}<td>{% if x.tg_chat %}<span class="pill a">Linked</span> <span class=mu>{{x.tg_chat}}</span>{% else %}<span class="pill e">Not linked</span><form class=row method=post action="/admin/reseller/{{x.id}}" style="margin-top:6px;flex-wrap:nowrap"><input type=hidden name=action value=tg><input name=tg_chat list=seenids placeholder="Chat ID" inputmode=numeric style="width:130px"><button class=g>Link</button></form>{% endif %}</td>{% endif %}
<td>{% if x.deleted %}<span class="pill e">Deleted</span>{% elif x.active %}<span class="pill a">Active</span>{% else %}<span class="pill e">Banned</span>{% endif %}</td>
<td style="white-space:nowrap">
{% if x.deleted %}
<form method=post action="/admin/account/{{x.id}}/restore" style="display:inline"><input type=hidden name=next value="{{base}}?st=deleted"><button class=g>Restore</button></form>
<form method=post action="/admin/account/{{x.id}}/purge" style="display:inline" onsubmit="return confirm('Delete {{x.username}} FOREVER? Keys history is lost.')"><input type=hidden name=next value="{{base}}?st=deleted"><button class=r>Delete forever</button></form>
{% else %}
<a class=btn href="/admin/reseller/{{x.id}}">Manage</a>
<form method=post action="/admin/account/{{x.id}}/{{'ban' if x.active else 'unban'}}" style="display:inline"><input type=hidden name=next value="{{base}}?st={{st}}"><button class="{{'o' if x.active else 'g'}}">{{'Ban' if x.active else 'Unban'}}</button></form>
<form method=post action="/admin/account/{{x.id}}/delete" style="display:inline" onsubmit="return confirm('Delete {{x.username}}? You can restore it from the Deleted tab.')"><input type=hidden name=next value="{{base}}?st={{st}}"><button class=r>Delete</button></form>
{% endif %}</td></tr>{% else %}<tr><td colspan=6>None</td></tr>{% endfor %}</table></div>
{% if kind!='user' %}<datalist id=seenids>{% for s in seen %}<option value="{{s.chat_id}}">{{s.name}} {{s.username}}</option>{% endfor %}</datalist>{% if seen and st=='active' %}<div class=card><h3>Pressed /start in the bot (not linked yet)</h3>{% for s in seen %}<span class="pill p" style="margin:2px">{{s.name or "?"}}{% if s.username %} @{{s.username}}{% endif %} &middot; {{s.chat_id}}</span>{% endfor %}</div>{% endif %}{% endif %}{% endblock %}"""

# ---- manage page buttons: ban/unban + delete/restore
old_btns_start = T["admin_reseller.html"].index("<div class=card><form method=post style=\"display:inline\"><input type=hidden name=action value=toggle>")
T["admin_reseller.html"] = T["admin_reseller.html"][:old_btns_start] + r"""<div class=card>
{% if r.deleted %}<span class="pill e">Deleted</span> <span class=mu>This account cannot login.</span><br><br>
<form method=post style="display:inline"><input type=hidden name=action value=restore><button class=g>Restore account</button></form>
<form method=post style="display:inline" onsubmit="return confirm('Delete FOREVER?')"><input type=hidden name=action value=purge><button class=r>Delete forever</button></form>
{% else %}<form method=post style="display:inline"><input type=hidden name=action value=toggle><button class="{{'o' if r.active else 'g'}}">{{'Ban account' if r.active else 'Unban account'}}</button></form>
<form method=post style="display:inline" onsubmit="return confirm('Delete this account? You can restore it later from the Deleted tab.')"><input type=hidden name=action value=delete><button class=r>Delete account</button></form>{% endif %}</div>{% endblock %}"""
sub("admin_reseller.html", '<a href="/admin/resellers">{{ic(\'back\',16)}} Back</a>',
    '<a href="{{\'/admin/users\' if r.role==\'user\' else \'/admin/resellers\'}}">{{ic(\'back\',16)}} Back</a>')

# ---- admin > Telegram: admin chat id only changes with a code
sub("admin_telegram.html",
    "<p class=mu>Your (admin) Telegram Chat ID &mdash; or simply open the bot and send <code>/admin YOUR_ADMIN_PASSWORD</code> and it fills itself. Device requests come here</p>\n<input name=admin_id value=\"{{admin_id}}\" placeholder=\"e.g. 123456789\" style=\"width:100%\" inputmode=numeric>\n", "")
sub("admin_telegram.html", "<div class=card><form method=post><input type=hidden name=action value=save>", r"""<div class=card><h3>{{ic('shield2',20)}} Admin Chat ID</h3>
<p class=mu>Every admin login sends a 6-digit code to this chat (cannot be switched off). Current: <code>{{admin_mask or 'not set'}}</code></p>
{% if chat_pending %}<p class=mu>A confirm code was sent to the NEW chat <code>{{chat_pending}}</code> <span id=cs style="color:#fbbf24">sending&hellip;</span></p>
<form class=row method=post><input type=hidden name=action value=chatid_confirm><input name=code inputmode=numeric maxlength=6 placeholder="6-digit code" required style="width:150px"><button class=g>Confirm</button></form>
<form method=post style="margin-top:8px"><input type=hidden name=action value=chatid_cancel><button class=o>Cancel</button></form>
<script>(function(){var n=0,d=document.getElementById('cs');async function p(){try{var j=await(await fetch('/admin/otp_status?k=-1',{cache:'no-store'})).json();
if(j.state==='ok'){d.style.color='#34d399';d.textContent='delivered';return}if(j.state==='fail'){d.style.color='#f87171';d.textContent='failed: '+j.err;return}}catch(e){}
if(++n<25)setTimeout(p,1200)}p()})();</script>
{% else %}<form class=row method=post><input type=hidden name=action value=chatid_start><input name=new_chat placeholder="New admin Chat ID" inputmode=numeric required style="width:230px"><button>Send code to new chat</button></form>
<p class=hint>The new chat must press START in the bot first. The change is saved only after you type the code it receives. The old chat is told about the change.</p>{% endif %}</div>
<div class=card><form method=post><input type=hidden name=action value=save>""")

# ---- admin verify page (same look as the reseller code page)
v = T["login_verify.html"]
v = v.replace("/login/otp_status", "/admin/otp_status?k=0").replace("<h1>Verification</h1>", "<h1>Admin Verification</h1>")
v = v.replace("Code sent to Telegram", "Admin code sent to Telegram")
T["admin_verify.html"] = v

# ---- admin first-time setup page (bot API token + admin chat id)
head = T["login_verify.html"][:T["login_verify.html"].index("<body>")]
T["admin_setup.html"] = head + r"""<body>
<div class="lg"><div class="box"><div class="logo-t">{{ic('bot',30)}}</div><h1>Connect your bot</h1><div class="dv"><i></i><u></u><i></i></div>
<div class="tag">{{ic('shield2',18)}} First-time admin setup</div>{% with m=get_flashed_messages(with_categories=true) %}{% for c,t in m %}<div class="flash {{c}}">{{t}}</div>{% endfor %}{% endwith %}
<form method=post autocomplete=off>
{% if need_token %}<label for=tk>Bot API token (from @BotFather)</label><div class="fld">{{ic('key',20)}}<input id=tk name=token type=password required placeholder="123456789:AAH..." autocomplete=off autofocus></div>{% endif %}
<label for=ci>Admin Telegram Chat ID</label><div class="fld">{{ic('user',20)}}<input id=ci name=chat_id value="{{chat_id}}" inputmode=numeric required pattern="-?[0-9]{5,15}"></div>
<div class="sess">{{ic('send',16)}} Open your bot in Telegram and press START first, so it can message you.</div>
<button class="go">CONNECT &amp; SEND CODE {{ic('arrow',20)}}</button></form>
<a href="/login/cancel" style="display:block;text-align:center;margin-top:14px;font-size:13px">&larr; Back to login</a>
<div class="copy">&copy; {{year}} {{BRAND}}</div></div></div></body></html>
"""

# ================================================================ v12 part 2
# ---- Reseller Update link for users (left three-line menu)
sub("rbase.html", """<a href="/wallet" class="{{'on' if page=='wallet'}}">{{ic('wallet')}} Add Balance</a>""",
    """<a href="/wallet" class="{{'on' if page=='wallet'}}">{{ic('wallet')}} Add Balance</a>
{% if r.role=='user' %}<a href="/upgrade" class="{{'on' if page=='upgrade'}}">{{ic('crown')}} Reseller Update</a>{% endif %}""")

T["upgrade.html"] = r"""{% extends 'rbase.html' %}{% block c %}
<h2 style="margin-top:14px">Reseller Update</h2><div class=mu>Upgrade your account to a RESELLER account.</div>
<div class=card style="text-align:center">
{% if price>0 and ready %}<div class=mu>One-time payment</div><div style="font-size:44px;font-weight:800;margin:6px 0">{{CURRENCY}}{{price}}</div>
<div class=tw style="text-align:left;max-width:360px;margin:8px auto"><div>&#10003; Reseller prices (cheaper than user prices)</div><div>&#10003; API &amp; Docs + API token</div><div>&#10003; Bot Make (your own bot)</div><div>&#10003; Security, alerts and all reseller tools</div></div>
<form method=post><button class=genb style="font-size:16px">{{ic('crown',20)}} Pay {{CURRENCY}}{{price}} &amp; become Reseller</button></form>
<p class=mu style="margin-top:10px">After the payment is verified your account becomes a reseller automatically. Your balance and key history stay.</p>
{% else %}<div class=mu>Reseller Update is not available right now. Please contact admin.</div>{% endif %}</div>{% endblock %}"""

# ---- payment page: same simple QR for Fampay and Paytm, instant
T["wallet_pay.html"] = r"""{% extends 'rbase.html' %}{% block c %}
<h2 style="margin-top:14px">{{'Reseller Update' if t.purpose=='upgrade' else 'Add wallet balance'}}</h2><div class=mu>Pay by UPI; it is applied only after secure verification.</div>
<a class="btn o" href="{{'/upgrade' if t.purpose=='upgrade' else '/wallet'}}" style="margin:12px 0;background:none;border:1px solid var(--bd);box-shadow:none">Back</a>
<div class=card style="text-align:center"><div class=mu style="text-align:left">Pending payment<br>{{t.order_id}}</div><div style="font-size:38px;font-weight:800;text-align:left">{{CURRENCY}}{{t.amount|money}}</div>
<div id=wait {{'hidden' if t.status!='pending'}}>
<div class=qrbox style="background:#fff;padding:12px;border-radius:14px;max-width:300px;margin:10px auto">{% if qr_svg %}<div style="width:100%">{{qr_svg}}</div>{% elif t.qr_url %}<img src="{{t.qr_url}}" alt="UPI QR" style="width:100%">{% else %}<div style="color:#000;padding:20px">QR not available</div>{% endif %}</div>
<div>Scan and pay <b>{{CURRENCY}}{{t.amount|money}}</b>{% if t.purpose=='upgrade' %} to become a reseller{% else %} to add it to your wallet{% endif %}.</div>
{% if t.upi_id %}<div class=mu style="margin-top:6px">UPI ID: <code>{{t.upi_id}}</code></div>{% endif %}
<div class=cd id=cd style="margin:10px 0">--:--</div>
{% if pay_uri %}<a class=btn href="{{pay_uri}}" style="margin:6px 0">Open UPI App</a><br>{% endif %}
{% if qr_svg or t.qr_url %}<a class=btn href="/wallet/qr/{{t.id}}" style="margin:6px 0">{{ic('download',18)}} Download QR</a>{% endif %}
{% if checkout and not qr_svg and not t.qr_url %}<a class=btn href="{{checkout}}" rel="noopener" style="margin:6px 0">Open payment page</a>{% endif %}
<p class=mu>Download the QR to pay from another device. Verification runs automatically for 5 minutes, even after you leave this page.</p></div>
<div id=ok {{'hidden' if t.status!='paid'}}><div style="font-size:54px">✅</div>
{% if t.purpose=='upgrade' %}<h3 style="justify-content:center">You are a Reseller now</h3><div class=mu>Payment verified. Reseller prices, API &amp; Docs and Bot Make are open.</div><a class=btn href="/dashboard" style="margin-top:12px">Open dashboard</a>
{% else %}<h3 style="justify-content:center">Payment successful</h3><div class=mu>{{CURRENCY}}{{t.amount|money}} added. New balance: <b id=nb style="color:#34d399">{{r.balance|cur}}</b></div>
<a class=btn href="/generate" style="margin-top:12px">{{ic('bolt',18)}} Generate keys</a>{% endif %}</div>
<div id=ex {{'hidden' if t.status!='expired'}}><h3 style="justify-content:center">QR expired</h3><div class=mu>If you already paid, it is still checked for a while. Otherwise create a new QR.</div><a class=btn href="{{'/upgrade' if t.purpose=='upgrade' else '/wallet'}}" style="margin-top:12px">New payment</a></div></div>
<script>
let left={{left}};const $=i=>document.getElementById(i),CU='{{CURRENCY}}';
function show(s,b){if(s==='paid'){$('wait').hidden=true;$('ex').hidden=true;$('ok').hidden=false;const n=$('nb');if(n)n.textContent=CU+(Math.round(b*100)/100);const e=$('sbal');if(e)e.textContent=CU+(Math.round(b*100)/100);clearInterval(T1);clearInterval(T2)}else if(s==='expired'){$('wait').hidden=true;$('ex').hidden=false}}
function tick(){if(left>0)left--;const m=Math.floor(left/60),s=left%60;$('cd').textContent=String(m).padStart(2,'0')+':'+String(s).padStart(2,'0')}
async function poll(){try{const j=await(await fetch('/wallet/status/{{t.id}}')).json();show(j.status,j.balance)}catch(e){}}
let T1,T2;if(!$('wait').hidden){tick();T1=setInterval(tick,1000);T2=setInterval(poll,3000)}
</script>{% endblock %}"""

# ---- admin gateway page: Fampay / Paytm toggle
T["admin_gateway.html"] = r"""{% extends 'abase.html' %}{% block c %}<h2>{{ic('qr',24)}} Payment Gateway</h2>
<div class=card><h3>Active gateway</h3>
<p class=mu>Only ONE gateway works at a time. Turning Paytm ON turns Fampay OFF; turning Paytm OFF turns Fampay back ON. Resellers and users see the same simple QR either way.</p>
<form method=post style="display:flex;gap:10px;flex-wrap:wrap;align-items:center"><input type=hidden name=action value=set_gw>
<button name=gw value=fam class="{{'g' if active=='fam' else 'o'}}">Fampay {{'● ON' if active=='fam' else 'OFF'}}</button>
<button name=gw value=paytm class="{{'g' if active=='paytm' else 'o'}}">Paytm {{'● ON' if active=='paytm' else 'OFF'}}</button></form></div>
<div class=card><h3>Amounts &amp; Reseller Update price</h3><form method=post><input type=hidden name=action value=save_common>
<p class=mu>Add-balance amounts shown to resellers/users (comma separated, e.g. <code>100, 200, 500, 1000</code>)</p><input name=amounts value="{{amounts}}" style="width:100%" inputmode=numeric>
<p class=mu>Reseller Update price (a user who pays this amount becomes a reseller). <b>0</b> = Reseller Update closed.</p><input name=upgrade_price value="{{upgrade_price}}" inputmode=numeric style="width:100%">
<button class=g style="margin-top:12px">{{ic('save')}} Save</button></form></div>
<div class=card><h3>Paytm gateway {% if active=='paytm' %}<span class="pill a">ON</span>{% endif %}</h3>
<form method=post><input type=hidden name=action value=save_zy>
<p class=mu>API key (full token <code>public.secret</code>){% if zy_tail %} &mdash; saved (ends with <code>{{zy_tail}}</code>). Leave empty to keep it.{% endif %}</p>
<input name=zy_key type=password autocomplete=off placeholder="public.secret" style="width:100%">
<p class=mu>Webhook secret{% if zy_wh %} &mdash; saved. Leave empty to keep it.{% endif %}</p><input name=zy_whsec type=password autocomplete=off style="width:100%">
<p class=mu>API URL</p><input name=zy_base value="{{zy_base}}" style="width:100%">
<p class=hint>Webhook URL to enter in your Paytm (ZYVO PAY) dashboard: <code>{{hook}}</code></p>
<button class=g style="margin-top:12px">{{ic('save')}} Save Paytm</button></form>
<form method=post style="margin-top:10px"><input type=hidden name=action value=test_zy><button {{'disabled' if not zy_ok}}>{{ic('qr')}} Generate Paytm test QR ({{CURRENCY}}1)</button></form></div>
<div class=card><h3>Fampay gateway {% if active=='fam' %}<span class="pill a">ON</span>{% endif %}</h3><form method=post><input type=hidden name=action value=save>
<p class=mu>Gateway URL</p><input name=base value="{{base}}" style="width:100%" required>
<p class=mu>UPI ID (your receiving ID, for your reference)</p><input name=upi value="{{upi}}" placeholder="yourid@fam" style="width:100%">
<p class=mu>API Token{% if tail %} &mdash; saved (ends with <code>{{tail}}</code>). Leave empty to keep it.{% endif %}</p>
<input name=token type=password autocomplete=off placeholder="FAM_xxxxxxxx" style="width:100%">
<button class=g style="margin-top:12px">{{ic('save')}} Save Fampay</button></form>
<form method=post style="margin-top:10px"><input type=hidden name=action value=test><button>{{ic('qr')}} Generate Fampay test QR ({{CURRENCY}}1)</button></form></div>
{% if test %}<div class=card><h3>{{test.who}} test</h3>{% if test.ok %}<div class="flash ok">QR created successfully. Order {{test.order}}</div>
<div style="background:#fff;padding:12px;border-radius:12px;max-width:260px">{% if test.svg %}{{test.svg}}{% elif test.img %}<img src="{{test.img}}" style="width:100%">{% endif %}</div>
{% else %}<div class="flash err">Failed: {{test.msg}}</div>{% endif %}</div>{% endif %}
<div class="card tw"><h3>Recent payments</h3><table><tr><th>User</th><th>Amount</th><th>For</th><th>Gateway</th><th>Status</th><th>Ref</th><th>Time</th></tr>
{% for t in tops %}<tr><td>{{t.username}}</td><td>{{t.amount|cur}}</td><td>{{'Reseller Update' if t.purpose=='upgrade' else 'Balance'}}</td><td>{{'Paytm' if t.provider=='zyvo' else 'Fampay'}}</td><td>{{t.status}}</td><td>{{t.utr or ''}}</td><td>{{t.created|dt}}</td></tr>{% else %}<tr><td colspan=7>None yet</td></tr>{% endfor %}</table></div>{% endblock %}"""

# ---- admin products: logo / premium emoji per product
sub("admin_products.html", """<h3>{{x.p.name}}</h3>""",
    """<h3 style="display:flex;align-items:center;gap:8px">{% if x.p.icon %}<img src="/picon/{{x.p.id}}?v={{x.p.icon_ver}}" style="width:26px;height:26px;border-radius:6px">{% elif x.p.emoji_id %}<img src="/emoji/{{x.p.emoji_id}}" style="width:26px;height:26px">{% endif %}{{x.p.name}}</h3>""")
sub("admin_products.html", """<div class=tw><table class=plans>""",
    """<details style="margin:6px 0 10px"><summary class=mu style="cursor:pointer">Logo / premium emoji</summary>
<form method=post enctype=multipart/form-data class=row style="margin-top:8px"><input type=hidden name=action value=product_icon><input type=hidden name=product_id value="{{x.p.id}}">
<input type=file name=icon accept="image/*" style="max-width:220px"><input name=emoji_id value="{{x.p.emoji_id}}" placeholder="Telegram premium emoji ID" inputmode=numeric style="width:230px">
<label class=mu><input type=checkbox name=remove_icon value=1 style="width:auto"> remove picture</label><button class=g>Save</button></form>
<p class=hint>Add a small picture OR paste a Telegram premium emoji ID (empty = none). It shows next to the product name for resellers and users.</p></details>
<div class=tw><table class=plans>""")

# ---- generate page: icon next to the product picker
sub("generate.html", """<div class=l>{{ic('box',22)}} Product type</div><select id=sp></select>""",
    """<div class=l>{{ic('box',22)}} Product type <span id=pic style="display:inline-flex;vertical-align:middle;margin-left:6px"></span></div><select id=sp></select>""")
sub("generate.html", "sp.onchange=fill;", "function pic(){const p=C[sp.value],e=$('pic');e.innerHTML='';if(p&&p.icon){const i=new Image();i.src=p.icon;i.style.cssText='width:26px;height:26px;border-radius:6px';i.onerror=()=>i.remove();e.appendChild(i)}}\nsp.onchange=()=>{fill();pic()};")
sub("generate.html", "C.forEach((p,i)=>sp.add(new Option(p.name,i)));", "C.forEach((p,i)=>sp.add(new Option(p.name,i)));setTimeout(()=>{try{pic()}catch(e){}},0);")

# ---- admin manage page: make reseller by hand
sub("admin_reseller.html", """<div class=card>
{% if r.deleted %}""", """{% if r.role=='user' and not r.deleted %}<div class=card><form method=post onsubmit="return confirm('Make this user a RESELLER?')"><input type=hidden name=action value=make_reseller><button class=g>Make Reseller</button> <span class=mu>(same as a paid Reseller Update)</span></form></div>{% endif %}
<div class=card>
{% if r.deleted %}""")

TEMPLATES = T
