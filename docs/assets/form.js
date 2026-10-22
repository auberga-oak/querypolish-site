(function(){
  var form=document.getElementById('intake');if(!form)return;
  var status=document.getElementById('status'),btn=document.getElementById('submit');
  var MSG='Please fill in the required fields marked with a star.';
  form.addEventListener('invalid',function(){status.className='err';status.textContent=MSG;},true);
  form.addEventListener('submit',function(e){
    e.preventDefault();
    status.className='';status.textContent='';
    if(!form.checkValidity()){
      form.reportValidity();
      var bad=form.querySelector('input:invalid,select:invalid,textarea:invalid');
      status.className='err';status.textContent=MSG;
      if(bad)bad.focus();
      return;
    }
    if(form.botcheck&&form.botcheck.checked)return;
    var data={};new FormData(form).forEach(function(v,k){data[k]=v;});
    btn.disabled=true;status.textContent='Sending...';
    fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)})
      .then(function(r){return r.json().then(function(j){return {ok:r.ok&&j.success!==false};});})
      .then(function(res){
        if(res.ok){window.location.href=new URL('thanks/',window.location.href).href;}
        else{throw new Error('rejected');}
      })
      .catch(function(){
        btn.disabled=false;status.className='err';
        status.textContent='Something went wrong and your details were not sent. Please try again in a few minutes.';
      });
  });
})();
