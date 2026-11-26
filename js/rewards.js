/* The Real Tours and Travels – coupons & reward points in the payment box (visa / passport pages) */
(function(){
  var W = window;
  function inr(n){ return '₹' + Math.round(n).toLocaleString('en-IN'); }
  function $(id){ return document.getElementById(id); }
  W.rttDisc = { coupon: null, points: 0, ref: null, service: null };

  W.rttApplyDisc = function(){
    var a = $('pt_amt'); if (!a) return;
    var base = +a.dataset.base || 0, d = W.rttDisc, off = 0, lines = [];
    if (d.coupon) { d.coupon.discount = Math.min(d.coupon.discount, base); off += d.coupon.discount; lines.push('Coupon ' + d.coupon.code + ' −' + inr(d.coupon.discount)); }
    if (d.points) { off += d.points; lines.push('Reward points −' + inr(d.points)); }
    var fin = Math.max(0, base - off);
    a.textContent = inr(fin); a.dataset.final = fin;
    var l = $('pt_disc_lines'); if (l) l.innerHTML = lines.length ? ('<s>' + inr(base) + '</s> · ' + lines.join(' · ')) : '';
    var wa = $('pt_wa');
    if (wa && d.ref) {
      var t = 'Hi The Real Tours and Travels, I have paid ' + inr(fin) + ' for reference ' + d.ref +
        (d.coupon ? ' (coupon ' + d.coupon.code + ')' : '') + (d.points ? ' (' + d.points + ' reward points used)' : '') + '. Sending the payment screenshot.';
      wa.href = 'https://wa.me/919843121212?text=' + encodeURIComponent(t);
    }
  };

  // Show the coupon / points box once the application has a reference number
  W.rttDiscBox = function(ref, service){
    var box = $('pt_disc'); if (!box) return;
    W.rttDisc.ref = ref; W.rttDisc.service = service || null;
    box.hidden = false;
    var cIn = $('pt_cin'), cBtn = $('pt_cbtn'), cMsg = $('pt_cmsg'), pW = $('pt_pts'), pMsg = $('pt_pmsg');
    if (!box.dataset.wired) {
      box.dataset.wired = 1;
      cBtn.addEventListener('click', function(){
        var code = (cIn.value || '').trim().toUpperCase(); if (!code) { cMsg.textContent = 'Enter a coupon code.'; return; }
        var base = +($('pt_amt').dataset.base || 0); cMsg.className = 'pdmsg'; cMsg.textContent = 'Checking…';
        W.rttClient().then(function(c){ return c.rpc('coupon_check', { c: code, amount: base, service: W.rttDisc.service }); })
          .then(function(r){
            var d = r && r.data;
            if (!d || !d.ok) { W.rttDisc.coupon = null; cMsg.className = 'pdmsg err'; cMsg.textContent = (d && d.msg) || 'This code is not valid.'; }
            else { W.rttDisc.coupon = { code: d.code, discount: +d.discount }; cMsg.className = 'pdmsg ok'; cMsg.textContent = '✅ ' + d.title + ' – you save ' + inr(d.discount); }
            W.rttApplyDisc();
          }).catch(function(){ cMsg.className = 'pdmsg err'; cMsg.textContent = 'Could not check the code. Please try again.'; });
      });
    }
    // reward points – only for logged-in customers
    pW.hidden = true;
    W.rttClient().then(function(c){
      return c.auth.getSession().then(function(s){
        if (!s.data.session) { pW.hidden = false; pW.innerHTML = '🎁 <a href="/account/">Log in</a> to use your reward points (new members get 100 points).'; return; }
        return c.rpc('reward_balance').then(function(r){
          var bal = +(r && r.data) || 0, base = +($('pt_amt').dataset.base || 0), use = Math.min(bal, Math.floor(base * 0.10));
          pW.hidden = false;
          if (W.rttDisc.points) { pW.innerHTML = '🎁 ' + W.rttDisc.points + ' reward points applied.'; return; }
          if (use <= 0) { pW.innerHTML = '🎁 You have ' + bal + ' reward points.' + (bal ? ' Points can pay up to 10% of a booking.' : ''); return; }
          pW.innerHTML = '🎁 You have <b>' + bal + '</b> reward points. <button type="button" class="btn outline" id="pt_pbtn">Use ' + use + ' points (−' + inr(use) + ')</button><span class="pdmsg" id="pt_pmsg"></span>';
          $('pt_pbtn').addEventListener('click', function(){
            var b = this; b.disabled = true;
            c.rpc('rewards_redeem', { pts: use, amount: base, ref: 'Order ' + ref }).then(function(x){
              if (x.error) { b.disabled = false; $('pt_pmsg').className = 'pdmsg err'; $('pt_pmsg').textContent = ' ' + x.error.message; return; }
              W.rttDisc.points = use; pW.innerHTML = '🎁 ' + use + ' reward points applied. Remaining balance: ' + x.data + ' points.'; W.rttApplyDisc();
            });
          });
        });
      });
    }).catch(function(){});
  };
})();
