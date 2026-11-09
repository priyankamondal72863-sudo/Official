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

TEMPLATES = T
