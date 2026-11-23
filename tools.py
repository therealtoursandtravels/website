"""Private GST quotation / proforma / tax-invoice maker (runs fully in the browser, stores nothing on a server)."""
import json

ITEMS = [
 # key, label, SAC, gst%, note
 ("pkg_dom", "Tour package – domestic (5%, no ITC)", "998552", 5, ""),
 ("pkg_intl", "Tour package – overseas (5% + 2% TCS)", "998552", 5, "tcs"),
 ("pkg_18", "Tour package – 18% (with ITC)", "998552", 18, ""),
 ("air_fare", "Air ticket fare – reimbursement (pure agent)", "", 0, "pa"),
 ("air_fee", "Air ticket service fee", "998551", 18, ""),
 ("hotel_pa", "Hotel charges – reimbursement (pure agent)", "", 0, "pa"),
 ("hotel_fee", "Hotel booking service fee", "998553", 18, ""),
 ("visa_gov", "Visa / passport / embassy fee – reimbursement (pure agent)", "", 0, "pa"),
 ("visa_fee", "Visa / passport service fee", "998559", 18, ""),
 ("ins_prem", "Travel insurance premium – reimbursement (pure agent)", "", 0, "pa"),
 ("cruise_pa", "Cruise fare – reimbursement (pure agent)", "", 0, "pa"),
 ("other_fee", "Other travel service / facilitation fee", "998559", 18, ""),
]

STATES = ["Maharashtra (27)","Andaman and Nicobar Islands (35)","Andhra Pradesh (37)","Arunachal Pradesh (12)","Assam (18)","Bihar (10)","Chandigarh (04)","Chhattisgarh (22)","Dadra and Nagar Haveli and Daman and Diu (26)","Delhi (07)","Goa (30)","Gujarat (24)","Haryana (06)","Himachal Pradesh (02)","Jammu and Kashmir (01)","Jharkhand (20)","Karnataka (29)","Kerala (32)","Ladakh (38)","Lakshadweep (31)","Madhya Pradesh (23)","Manipur (14)","Meghalaya (17)","Mizoram (15)","Nagaland (13)","Odisha (21)","Puducherry (34)","Punjab (03)","Rajasthan (08)","Sikkim (11)","Tamil Nadu (33)","Telangana (36)","Tripura (16)","Uttar Pradesh (09)","Uttarakhand (05)","West Bengal (19)","Other country (export)"]

def gst_tool_page(NAME, ADDR, GST, PHONE, EMAIL):
    opts = "".join(f'<option value="{k}">{l}</option>' for k,l,_,_,_ in ITEMS)
    st = "".join(f"<option>{x}</option>" for x in STATES)
    return f"""
<section class="no-print" style="padding:34px 0 10px"><div class="wrap">
<h1 style="font-size:clamp(28px,4vw,40px);color:var(--wine);margin:0 0 6px">GST Quote &amp; Invoice Maker</h1>
<p class="meta">Private tool for The Real Tours and Travels team. Everything runs in this browser – nothing is saved online. Fill the details, then Print / Save as PDF or copy the WhatsApp summary.</p>
<div class="qt-form">
<div class="qrow">
<label>Document<select id="q_doc"><option>Quotation</option><option>Proforma Invoice</option><option>Tax Invoice</option></select></label>
<label>Number<input id="q_no" maxlength="30"></label>
<label>Date<input id="q_date" type="date"></label>
<label>Valid till / Due date<input id="q_due" type="date"></label></div>
<div class="qrow">
<label>Client name*<input id="q_client" maxlength="120" placeholder="Client / company name"></label>
<label>Client phone / email<input id="q_contact" maxlength="120"></label>
<label>Client GSTIN (if B2B)<input id="q_cgstin" maxlength="15" placeholder="optional" style="text-transform:uppercase"></label>
<label>Place of supply<select id="q_pos">{st}</select></label></div>
<label>Client address<input id="q_addr" maxlength="200" placeholder="optional"></label>
<label>Trip / reference<input id="q_trip" maxlength="160" placeholder="e.g. Kashmir 5N/6D, 20–25 Dec, 4 adults"></label>
<table class="qlines"><thead><tr><th>Item type</th><th>Description</th><th>Qty</th><th>Rate (₹)</th><th>GST %</th><th></th></tr></thead><tbody id="q_body"></tbody></table>
<div class="btns"><button class="btn outline" type="button" id="q_add">+ Add line</button></div>
<div class="qrow"><label>TCS % on overseas package<input id="q_tcs" type="number" min="0" step="0.1" value="2"></label>
<label>Round off total<select id="q_round"><option value="1">Yes</option><option value="0">No</option></select></label>
<label style="grid-column:span 2">Notes / terms<input id="q_notes" maxlength="300" value="Prices valid subject to availability at the time of booking. Airline, hotel, visa and insurance amounts are actual costs paid on your behalf as pure agent."></label></div>
<div class="btns"><button class="btn gold" type="button" onclick="window.print()">🖨️ Print / Save PDF</button><button class="btn ghost" type="button" id="q_wa">💬 Copy WhatsApp summary</button><span id="q_copied" class="meta"></span></div>
<p class="meta">GST rules used: tour packages 5% without ITC (or 18% with ITC); service fees / commission 18%; government, embassy, airline, hotel, insurance and cruise amounts passed through at actual cost as pure agent (no GST added by us – keep supplier invoices); CGST + SGST for Maharashtra, IGST for other states; 2% TCS on overseas tour packages (Income-tax Act, 2025, from 1 April 2026). Confirm your billing structure with your Chartered Accountant.</p>
</div></div></section>

<section style="padding:10px 0 60px"><div class="wrap"><div class="doc" id="doc"></div></div></section>
<script>
(function(){{
const ITEMS={json.dumps({k:{"label":l,"sac":sac,"gst":g,"note":n} for k,l,sac,g,n in ITEMS})};
const $=i=>document.getElementById(i),body=$('q_body');
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[c]);
const inr=n=>'₹'+(+n).toLocaleString('en-IN',{{minimumFractionDigits:2,maximumFractionDigits:2}});
const r2=n=>Math.round(n*100)/100;
const today=new Date(Date.now()+330*6e4).toISOString().slice(0,10);
function store(k,v){{try{{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}}catch(_){{return null;}}}}
const yr=(()=>{{const d=new Date(),y=d.getMonth()>=3?d.getFullYear():d.getFullYear()-1;return String(y).slice(2)+'-'+String(y+1).slice(2);}})();
const seq=(+store('rt_q_seq')||0)+1;
$('q_no').value='RTT/'+yr+'/'+String(seq).padStart(3,'0');$('q_date').value=today;
$('q_due').value=new Date(Date.now()+330*6e4+7*864e5).toISOString().slice(0,10);
function addLine(type,desc,qty,rate){{
 const tr=document.createElement('tr');
 tr.innerHTML='<td><select class="l_type">{opts}</select></td><td><input class="l_desc" maxlength="160"></td><td><input class="l_qty" type="number" min="0" step="1" value="1"></td><td><input class="l_rate" type="number" min="0" step="0.01"></td><td><input class="l_gst" type="number" min="0" max="28" step="0.5"></td><td><button type="button" class="l_del" aria-label="Remove line">✕</button></td>';
 body.appendChild(tr);
 const t=tr.querySelector('.l_type');t.value=type||'pkg_dom';
 tr.querySelector('.l_gst').value=ITEMS[t.value].gst;tr.querySelector('.l_desc').value=desc||'';
 if(qty)tr.querySelector('.l_qty').value=qty;if(rate)tr.querySelector('.l_rate').value=rate;
 t.addEventListener('change',()=>{{tr.querySelector('.l_gst').value=ITEMS[t.value].gst;render();}});
 tr.querySelector('.l_del').addEventListener('click',()=>{{tr.remove();render();}});
 tr.querySelectorAll('input').forEach(i=>i.addEventListener('input',render));
}}
$('q_add').addEventListener('click',()=>{{addLine('other_fee');render();}});
addLine('pkg_dom','Holiday package as per itinerary',1,'');addLine('air_fare','Air tickets',1,'');addLine('air_fee','Ticketing service fee',1,'');
document.querySelectorAll('.qt-form input,.qt-form select').forEach(i=>i.addEventListener('input',render));
function words(n){{
 const a=['','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen'],b=['','','Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety'];
 const two=x=>x<20?a[x]:b[Math.floor(x/10)]+(x%10?' '+a[x%10]:''),three=x=>(x>=100?a[Math.floor(x/100)]+' Hundred'+(x%100?' ':''):'')+(x%100?two(x%100):'');
 if(n===0)return 'Zero';let s='',cr=Math.floor(n/1e7);n%=1e7;let l=Math.floor(n/1e5);n%=1e5;let t=Math.floor(n/1e3);n%=1e3;
 if(cr)s+=(cr>99?words(cr):two(cr))+' Crore ';if(l)s+=two(l)+' Lakh ';if(t)s+=two(t)+' Thousand ';if(n)s+=three(n);return s.trim();
}}
function calc(){{
 const pos=$('q_pos').value,intra=pos.startsWith('Maharashtra'),exp=pos.startsWith('Other country');
 let lines=[],taxable=0,pa=0,tax=0,tcsBase=0;
 body.querySelectorAll('tr').forEach(tr=>{{
  const k=tr.querySelector('.l_type').value,it=ITEMS[k],q=Math.max(0,+tr.querySelector('.l_qty').value||0),r=Math.max(0,+tr.querySelector('.l_rate').value||0);
  let g=it.note==='pa'?0:Math.max(0,+tr.querySelector('.l_gst').value||0);if(exp&&it.note!=='pa')g=0;
  const amt=r2(q*r),gst=r2(amt*g/100);
  if(it.note==='pa')pa+=amt;else{{taxable+=amt;tax+=gst;}}
  if(it.note==='tcs')tcsBase+=amt+gst;
  lines.push({{k,label:it.label,desc:tr.querySelector('.l_desc').value,sac:it.sac,q,r,g,amt,gst,pa:it.note==='pa'}});
 }});
 const tcs=r2(tcsBase*Math.max(0,+$('q_tcs').value||0)/100);
 let total=r2(taxable+tax+pa+tcs),round=0;if($('q_round').value==='1'){{round=r2(Math.round(total)-total);total=Math.round(total);}}
 return {{lines,taxable:r2(taxable),pa:r2(pa),tax:r2(tax),tcs,round,total,intra,exp,pos}};
}}
function render(){{
 const c=calc(),doc=$('q_doc').value,cg=$('q_cgstin').value.trim().toUpperCase();
 const gstRows=c.exp?'<tr><td colspan="2">Export of service / zero-rated (confirm LUT)</td><td>₹0.00</td></tr>':(c.intra?'<tr><td colspan="2">CGST</td><td>'+inr(c.tax/2)+'</td></tr><tr><td colspan="2">SGST</td><td>'+inr(c.tax/2)+'</td></tr>':'<tr><td colspan="2">IGST</td><td>'+inr(c.tax)+'</td></tr>');
 const rows=c.lines.map((l,i)=>'<tr><td>'+(i+1)+'</td><td><b>'+esc(l.desc||l.label)+'</b><br><small>'+esc(l.label)+'</small></td><td>'+(l.sac||'–')+'</td><td>'+l.q+'</td><td>'+inr(l.r)+'</td><td>'+inr(l.amt)+'</td><td>'+(l.pa?'Pure agent':l.g+'%')+'</td><td>'+inr(l.gst)+'</td><td>'+inr(l.amt+l.gst)+'</td></tr>').join('');
 $('doc').innerHTML='<div class="dhead"><img src="../../img/logo.png" alt="" width="84" height="84"><div><b>{NAME}</b><small>{", ".join(ADDR)}</small><small>📞 {PHONE} · ✉️ {EMAIL} · www.therealtoursandtravels.com</small><small><strong>GSTIN: {GST}</strong> · State: Maharashtra (27)</small></div><div class="dtype">'+esc(doc.toUpperCase())+'<small>No. '+esc($('q_no').value)+'</small><small>Date: '+esc($('q_date').value.split('-').reverse().join('-'))+'</small>'+($('q_due').value?'<small>'+(doc==='Quotation'?'Valid till':'Due')+': '+esc($('q_due').value.split('-').reverse().join('-'))+'</small>':'')+'</div></div>'+
 '<div class="dparty"><div><small>BILL TO</small><b>'+esc($('q_client').value||'Client name')+'</b>'+($('q_addr').value?'<span>'+esc($('q_addr').value)+'</span>':'')+($('q_contact').value?'<span>'+esc($('q_contact').value)+'</span>':'')+(cg?'<span>GSTIN: '+esc(cg)+'</span>':'')+'</div><div><small>PLACE OF SUPPLY</small><b>'+esc(c.pos)+'</b>'+($('q_trip').value?'<small style="margin-top:8px">TRIP / REFERENCE</small><span>'+esc($('q_trip').value)+'</span>':'')+'</div></div>'+
 '<table class="dlines"><thead><tr><th>#</th><th>Description</th><th>SAC</th><th>Qty</th><th>Rate</th><th>Taxable / Amount</th><th>GST</th><th>GST amt</th><th>Total</th></tr></thead><tbody>'+rows+'</tbody></table>'+
 '<div class="dsum"><div class="dwords"><small>AMOUNT IN WORDS</small><b>Rupees '+words(Math.floor(c.total))+(Math.round((c.total%1)*100)?' and '+words(Math.round((c.total%1)*100))+' Paise':'')+' Only</b>'+
 '<p>'+esc($('q_notes').value)+'</p>'+(c.tcs?'<p>TCS collected under the Income-tax Act on overseas tour package – credit available in your Form 26AS / AIS.</p>':'')+'</div>'+
 '<table class="dtot"><tr><td colspan="2">Taxable value</td><td>'+inr(c.taxable)+'</td></tr>'+gstRows+'<tr><td colspan="2">Reimbursements (pure agent)</td><td>'+inr(c.pa)+'</td></tr>'+(c.tcs?'<tr><td colspan="2">TCS @ '+(+$('q_tcs').value)+'%</td><td>'+inr(c.tcs)+'</td></tr>':'')+(c.round?'<tr><td colspan="2">Round off</td><td>'+inr(c.round)+'</td></tr>':'')+'<tr class="grand"><td colspan="2">Grand total</td><td>'+inr(c.total)+'</td></tr></table></div>'+
 '<div class="dfoot"><div>'+(doc==='Tax Invoice'?'Tax is payable on reverse charge: No':'This is a '+esc(doc.toLowerCase())+', not a tax invoice.')+'<br>Subject to Mumbai jurisdiction.</div><div class="dsign">For {NAME}<br><br><br>Authorised Signatory</div></div>';
}}
$('q_wa').addEventListener('click',async()=>{{
 const c=calc();const t=$('q_doc').value+' '+$('q_no').value+' – The Real Tours and Travels\\n'+($('q_trip').value?'Trip: '+$('q_trip').value+'\\n':'')+c.lines.filter(l=>l.amt).map(l=>'• '+(l.desc||l.label)+': '+inr(l.amt)+(l.gst?' + GST '+inr(l.gst):'')).join('\\n')+'\\n'+(c.exp?'':(c.intra?'CGST+SGST: ':'IGST: ')+inr(c.tax)+'\\n')+(c.tcs?'TCS: '+inr(c.tcs)+'\\n':'')+'Total: '+inr(c.total)+'\\n\\nPay securely: www.therealtoursandtravels.com/visa/#pay\\nCall/WhatsApp {PHONE}';
 try{{await navigator.clipboard.writeText(t);$('q_copied').textContent='Copied ✓';}}catch(_){{prompt('Copy this text:',t);}}
}});
window.addEventListener('beforeprint',()=>{{const n=$('q_no').value.match(/(\\d+)$/);if(n)store('rt_q_seq',String(Math.max(+n[1],+store('rt_q_seq')||0)));}});
render();
}})();
</script>"""

TOOL_CSS = """
.qt-form{display:grid;gap:14px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px}
.qrow{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.qt-form label{display:grid;gap:5px;font-size:13px;font-weight:600;color:var(--wine)}
.qt-form input,.qt-form select{font:400 15px 'Jost',sans-serif;padding:9px 10px;border:1px solid var(--line);border-radius:10px;width:100%;min-width:0;background:#fff}
.qlines{width:100%;border-collapse:collapse}.qlines th{text-align:left;font-size:12px;color:var(--muted);padding:6px 4px}.qlines td{padding:4px}
.qlines td:nth-child(1){width:30%}.qlines td:nth-child(3),.qlines td:nth-child(5){width:80px}.qlines td:nth-child(4){width:120px}
.l_del{border:0;background:#fdf0f0;color:var(--crimson);border-radius:8px;width:34px;height:36px;cursor:pointer}
.qt-form button.btn{border:0;cursor:pointer;font-family:inherit}.qt-form .btn.outline{border:1.5px solid var(--crimson);background:#fff}.qt-form .btn.ghost{border:1.5px solid var(--ink);background:#fff}
.doc{background:#fff;border:1px solid var(--line);border-radius:14px;padding:30px;max-width:980px;margin:0 auto;font-size:13.5px;color:#222;border-top:6px solid var(--red)}
.dhead{display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:center;border-bottom:2px solid var(--wine);padding-bottom:14px}
.dhead>div>b{font-family:'Playfair Display',serif;font-size:22px;color:var(--crimson)}.dhead small{display:block;color:#444;font-size:12px;margin-top:2px}
.dtype{text-align:right;font-weight:700;font-size:18px;letter-spacing:2px;color:var(--wine)}.dtype small{display:block;font-weight:400;letter-spacing:0;font-size:12.5px;color:#444}
.dparty{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:14px 0;border-bottom:1px solid var(--line)}.dparty small{display:block;color:var(--muted);font-size:11px;letter-spacing:1px}.dparty b{display:block;font-size:15px}.dparty span{display:block}
.dlines{width:100%;border-collapse:collapse;margin-top:14px}.dlines th{background:#fdf0f0;color:var(--crimson);font-size:11.5px;text-align:left;padding:8px 6px}.dlines td{padding:8px 6px;border-bottom:1px solid var(--line);vertical-align:top}.dlines small{color:var(--muted);font-size:11px}
.dlines td:nth-child(n+4),.dlines th:nth-child(n+4){text-align:right;white-space:nowrap}
.dsum{display:grid;grid-template-columns:1.2fr 1fr;gap:20px;margin-top:14px}.dwords small{display:block;color:var(--muted);font-size:11px;letter-spacing:1px;margin-bottom:4px}.dwords p{font-size:12px;color:#555}
.dtot{width:100%;border-collapse:collapse}.dtot td{padding:6px;border-bottom:1px solid var(--line)}.dtot td:last-child{text-align:right;white-space:nowrap}.dtot .grand td{font-weight:700;font-size:16px;color:var(--crimson);border-top:2px solid var(--wine);border-bottom:0}
.dfoot{display:flex;justify-content:space-between;gap:20px;margin-top:24px;font-size:12px;color:#555}.dsign{text-align:right;font-weight:600;color:#222}
@media(max-width:800px){.qrow{grid-template-columns:1fr 1fr}.qlines thead{display:none}.qlines tr{display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:6px;border-bottom:1px solid var(--line);padding:8px 0}.qlines td{width:auto!important}.qlines td:nth-child(1),.qlines td:nth-child(2){grid-column:1/-1}.doc{padding:16px;overflow-x:auto}}
@media print{.no-print{display:none!important}.doc{border:0;box-shadow:none;padding:0;max-width:none}section{padding:0!important}}
"""
