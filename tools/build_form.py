"""Builds the intake <form> inside docs/index.html (branching v1). Run: python3 tools/build_form.py"""
import re
A,B,C='local_listing','local_no_listing','online_only'
def rid(n): return re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
def f(name,label,typ="text",req=False,breq=False,hint="",ph="",extra="",auto=""):
    """req: always required. breq: required only while its branch is shown (JS adds `required`)."""
    i=rid(name)
    if req: mark=' <span class="req" aria-hidden="true">*</span>'
    elif breq: mark=' <span class="req req-js" aria-hidden="true">*</span><span class="opt nojs-only">(required if this is your answer above)</span>'
    else: mark=' <span class="opt">(optional)</span>'
    h=f'<span class="hint" id="{i}-h">{hint}</span>' if hint else ''
    d=f' aria-describedby="{i}-h"' if hint else ''
    r=' required' if req else (' data-breq' if breq else '')
    a=f' autocomplete="{auto}"' if auto else ''; p=f' placeholder="{ph}"' if ph else ''
    inp=(f'<textarea id="{i}" name="{name}"{r}{d}{p}{extra}></textarea>' if typ=="textarea"
         else f'<input id="{i}" name="{name}" type="{typ}"{r}{d}{a}{p}{extra}>')
    return f'<div class="f"><label for="{i}">{label}{mark}{h}</label>{inp}</div>'
def g(cls,*x): return f'<div class="{cls}">'+''.join(x)+'</div>'
def br(branches,inner,tag="div",cls=""):
    c=f' class="{cls}"' if cls else ''
    return f'<{tag} data-branch="{" ".join(branches)}"{c}>{inner}</{tag}>'
LETTER={A:'A',B:'B',C:'C'}
def nojs(branches):
    return '<p class="hint nojs-only">Fill in this part if you picked '+' or '.join(LETTER[b] for b in branches)+' above.</p>'
out=[]
# Q1
out.append('<fieldset id="q1"><legend>How do your customers find and use your business? <span class="req" aria-hidden="true">*</span></legend>'
 '<p class="hint" id="q1-h">Not sure? If you can be found on Google Maps, pick A.</p>'
 '<div class="choices" role="radiogroup" aria-describedby="q1-h">'
 f'<label class="check" for="bt-a"><input id="bt-a" type="radio" name="business_type" value="{A}" required><span><b>A. I\'m a local business with a Google Maps listing</b> (customers visit me, or I visit them in my area)</span></label>'
 f'<label class="check" for="bt-b"><input id="bt-b" type="radio" name="business_type" value="{B}"><span><b>B. I\'m a local business but I don\'t have a Google Maps listing yet</b></span></label>'
 f'<label class="check" for="bt-c"><input id="bt-c" type="radio" name="business_type" value="{C}"><span><b>C. I\'m online only</b> (no shop or service area, e.g. e-commerce, SaaS, newsletter, online courses)</span></label>'
 '</div></fieldset>')
# Common business basics
out.append('<fieldset><legend>Your business</legend>'+
 f("Business name","Business name",req=True,hint="Exactly as it appears on your Google Business Profile, if you have one.",auto="organization")+
 f("Owner name","Owner's name",auto="name")+
 g("grid2",f("Year founded","Year founded","number",extra=' min="1800" max="2026" inputmode="numeric"'),
   '<div class="f"><label for="team-size">Team size <span class="opt">(optional)</span></label><select id="team-size" name="Team size"><option value="">Choose one</option><option>Solo</option><option>Small team</option><option>Large team</option></select></div>')+
 f("Target customer","Your best customer",typ="textarea",hint="Who they are, in a sentence or two.")+
 '</fieldset>')
# Branch A: listing
out.append(br([A],'<legend>Your Google Maps listing</legend>'+nojs([A])+
 f("Google Business Profile URL","Your Google Business Profile link","url",breq=True,hint="Open your listing in Google Maps and copy the share link.",ph="https://")+
 f("Address","Full address",hint="Include suite or unit number. Write it as it appears on your profile.",auto="street-address"),tag="fieldset"))
# Branch B: no listing
out.append(br([B],'<legend>Where you work</legend>'+nojs([B])+
 f("Address or service area","Business address or service area",breq=True,hint="Your street address if customers visit you, or the area you cover if you visit them.",auto="street-address"),tag="fieldset"))
# Branch A+B: local services and market
out.append(br([A,B],'<legend>Services and market</legend>'+nojs([A,B])+
 g("grid2",f("Phone","Phone number","tel",hint="As shown on your profile or website.",auto="tel"),f("Industry","Industry or type of business",ph="e.g. plumber, dental clinic"))+
 f("Website","Website address","url",ph="https://",auto="url")+
 f("Main service","Main service",ph="e.g. emergency plumbing")+
 f("Other services","Other services",typ="textarea",hint="Up to 5, one per line.")+
 f("Cities served","Cities you serve",typ="textarea",hint="Up to 5, one per line. Put your main city first.")+
 br([A],f("Neighbourhoods","Neighbourhoods or areas",typ="textarea",hint="Up to 3, one per line. These are the parts of town where you most want to be found."))+
 f("Average job value","Average job value",hint="Roughly, with currency, e.g. 4,000 SEK."),tag="fieldset"))
# Branch C: online
out.append(br([C],'<legend>Your online business</legend>'+nojs([C])+
 f("Website (online)","Website address","url",breq=True,ph="https://",auto="url")+
 f("What you sell","What you sell",typ="textarea",hint="Your main products or services, in a sentence or two.")+
 g("grid2",f("Main country","Main country",hint="Where most of your customers are.",auto="country-name"),f("Main language","Main language",hint="The language your customers search in."))
 ,tag="fieldset"))
# Competitors (all optional; GBP only in A)
comps=''
for i in range(1,4):
    comps+=(f'<div class="comp"><h3>Competitor {i}</h3>'+f(f"Competitor {i} name","Name")+
      g("grid2",f(f"Competitor {i} domain","Website domain",ph="example.com"),
        br([A],f(f"Competitor {i} GBP URL","Google Business Profile link","url",ph="https://")))+
      f(f"Competitor {i} why they beat you","Why they beat you, if you know",typ="textarea")+'</div>')
out.append('<fieldset><legend>Competitors <span class="opt">(optional)</span></legend><p class="hint">Up to three businesses that most often show up above you in search. The more you name, the better the audit.</p>'+comps+'</fieldset>')
# Keywords: all branches, all optional; review words only A
kw=[f(f"Keyword {i}",f"Keyword {i}") for i in range(1,6)]
out.append('<fieldset><legend>Keywords <span class="opt">(all optional)</span></legend><p class="hint" id="kw-h">The searches you most want to show up for, such as "plumber in Uppsala". Up to five.</p>'+
 g("grid2",*kw[:2])+g("grid2",*kw[2:4])+kw[4]+
 f("Keywords you rank for now","Searches you already show up for",typ="textarea",hint="If you know them.")+
 f("Keywords you should rank for","Searches you should show up for but don't",typ="textarea")+
 br([A],g("grid2",f("Review service keyword","Service word for reviews",hint="The service you'd like customers to mention in reviews."),f("Review city keyword","City word for reviews",hint="The place you'd like customers to mention in reviews.")))+
 '</fieldset>')
# Numbers: Google-profile ones only A
out.append('<fieldset><legend>Your current numbers <span class="opt">(all optional)</span></legend><p class="hint">Fill in what you know. Leave the rest blank.</p>'+
 br([A],g("grid3",f("Google reviews total","Google reviews","number",extra=' min="0" inputmode="numeric"'),f("Star rating","Star rating","number",extra=' min="1" max="5" step="0.1" inputmode="decimal"'),f("New reviews per month","New reviews a month","number",extra=' min="0" inputmode="numeric"'))+
   f("Monthly profile views","Monthly views of your Google profile","number",extra=' min="0" inputmode="numeric"')+
   f("Map pack status","Google Maps top 3",typ="textarea",hint="Which searches you show up in the top 3 for, and which you don't."))+
 f("Monthly website visits","Monthly website visits","number",extra=' min="0" inputmode="numeric"')+
 f("Biggest SEO problem","Your biggest search problem, in one sentence")+
 f("SEO already tried","What you've already tried",typ="textarea",hint="Agency, do-it-yourself, tools. What worked and what didn't.")+
 '</fieldset>')
# Common: report
out.append('<fieldset><legend>Where to send the report</legend>'+
 f("email","Your email address","email",req=True,auto="email")+
 '<div class="f" role="radiogroup" aria-labelledby="lang-l"><span class="lbl" id="lang-l">Report language</span><div class="choices row">'
 '<label class="check" for="lang-en"><input id="lang-en" type="radio" name="report_language" value="English" checked><span>English</span></label>'
 '<label class="check" for="lang-sv"><input id="lang-sv" type="radio" name="report_language" value="Swedish"><span>Swedish</span></label></div></div>'+
 '<div class="f"><label class="check" for="consent"><input id="consent" name="Consent" type="checkbox" value="Yes" required><span>I agree that Finansium AB may use the information in this form to prepare my audit and email it to me, as described in the <a href="/privacy/">privacy note</a>. <span class="req" aria-hidden="true">*</span></span></label></div>'+
 '</fieldset>')
html=open('docs/index.html').read()
start=html.index('<div class="hp"'); start=html.index('</div>',start)+len('</div>\n')
end=html.index('<button type="submit" id="submit">')
html=html[:start]+"\n".join(out)+"\n"+html[end:]
open('docs/index.html','w').write(html)
print('ok', len(out),'blocks')
