() => {
 const parse=c=>{const m=c.match(/rgba?\(([^)]+)\)/);if(!m)return null;const a=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);return {r:a[0],g:a[1],b:a[2],a:a.length>3?a[3]:1}};
 const lum=({r,g,b})=>{const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)};return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)};
 const bgOf=el=>{while(el){const c=parse(getComputedStyle(el).backgroundColor);if(c&&c.a>0.5)return c;el=el.parentElement}return {r:255,g:255,b:255,a:1}};
 const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
 while(w.nextNode()){const t=w.currentNode;if(!t.textContent.trim())continue;const el=t.parentElement;const cs=getComputedStyle(el);
  const r=el.getBoundingClientRect();if(r.width===0||cs.visibility==='hidden'||r.left<-1000)continue;
  const fg=parse(cs.color),bg=bgOf(el);const L1=lum(fg),L2=lum(bg);const ratio=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
  const px=parseFloat(cs.fontSize),wt=parseInt(cs.fontWeight);out.push({text:t.textContent.trim().slice(0,40),fg:cs.color,bg:`rgb(${bg.r}, ${bg.g}, ${bg.b})`,ratio:Math.round(ratio*100)/100,large:px>=24||(px>=18.66&&wt>=700)})}
 // placeholders
 document.querySelectorAll('[placeholder]').forEach(e=>{const c=parse(getComputedStyle(e,'::placeholder').color),bg=bgOf(e);if(!c)return;const L1=lum(c),L2=lum(bg);out.push({text:'placeholder:'+e.placeholder,fg:getComputedStyle(e,'::placeholder').color,bg:'input',ratio:Math.round((Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05)*100)/100,large:false})});
 return out;}
