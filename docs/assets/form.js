(function(){
  var form=document.getElementById('intake');if(!form)return;
  var status=document.getElementById('status'),btn=document.getElementById('submit');
  var MSG='Please fill in the required fields marked with a star.';
  // Branching: sections tagged data-branch="..." show only for those business_type values.
  // Controls inside an inactive section are disabled (so not validated and not submitted)
  // and lose `required`; data-breq marks fields that are required while their section is shown.
  function current(){var r=form.querySelector('input[name="business_type"]:checked');return r?r.value:'';}
  function update(){
    var v=current(),secs=form.querySelectorAll('[data-branch]');
    for(var i=0;i<secs.length;i++){secs[i].hidden=secs[i].getAttribute('data-branch').split(' ').indexOf(v)<0;}
    var els=form.elements;
    for(var j=0;j<els.length;j++){
      var el=els[j],on=true,p=el.parentElement;
      while(p&&p!==form){if(p.hasAttribute('data-branch')&&p.getAttribute('data-branch').split(' ').indexOf(v)<0){on=false;break;}p=p.parentElement;}
      if(el.tagName==='FIELDSET')continue;
      el.disabled=!on;
      if(el.hasAttribute('data-breq'))el.required=on;
    }
  }
  form.addEventListener('change',function(e){if(e.target.name==='business_type')update();});
  update();
  form.addEventListener('invalid',function(){status.className='err';status.textContent=MSG;},true);
  form.addEventListener('submit',function(e){
    e.preventDefault();
    status.className='';status.textContent='';
    update();
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
        if(res.ok){window.location.href='/thanks/';}
        else{throw new Error('rejected');}
      })
      .catch(function(){
        btn.disabled=false;status.className='err';
        status.textContent='Something went wrong and your details were not sent. Please try again in a few minutes.';
      });
  });
})();
