
const weapons=[
{id:"wam",name:"ワム槍",rate:20,boosted:false,img:"/static/tools/granbluefantasy/img/wamuspear.png"},
{id:"olu",name:"オルオベ<br>冬ノ霜柱",rate:6.5,boosted:true,img:"/static/tools/granbluefantasy/img/oluobe.png"},
{id:"mare",name:"マレ斧",rate:3,boosted:true,img:"/static/tools/granbluefantasy/img/mareaxe.png"},
{id:"levi",name:"リヴァ槍",rate:11,boosted:true,img:"/static/tools/granbluefantasy/img/leviathan_spear.png"}];

const counts={wam:0,olu:0,mare:0,levi:0,boost:0};
let mainBonus=170,friendBonus=170;

document.getElementById("weapon-list").innerHTML=weapons.map(w=>`
<div class="weapon-card">
 <img class="item-image" src="${w.img}" alt="${w.name.replace(/<br>/g,"・")}">
 <div>
  <span class="name">${w.name}</span>
  <span class="pct">${w.rate}%${w.boosted?"":"・加護対象外"}</span>
 </div>
 <div class="controls">
  <button type="button" data-id="${w.id}" data-d="-1">−</button>
  <strong id="${w.id}-count">0</strong>
  <button type="button" data-id="${w.id}" data-d="1">＋</button>
 </div>
</div>`).join("");

const fmt=n=>Number(n.toFixed(2)).toString();

function calc(){
 let fixed=0,base=0;
 weapons.forEach(w=>{
  const v=w.rate*counts[w.id];
  w.boosted ? base+=v : fixed+=v;
 });
 const mult=
  mainBonus+
  friendBonus+
  counts.boost*20+
  (document.getElementById("gab").classList.contains("active")?20:0)+
  (document.getElementById("uruki").classList.contains("active")?10:0)+
  (document.getElementById("kusabi").classList.contains("active")?30:0);

 document.getElementById("rate").textContent=fmt(fixed+base*(1+mult/100))+"%";
}

document.addEventListener("click",e=>{
 const c=e.target.closest("[data-id]");
 if(c){
  const id=c.dataset.id;
  counts[id]=Math.max(0,counts[id]+Number(c.dataset.d));
  document.getElementById(id+"-count").textContent=counts[id];
  if(id==="boost"){
   document.getElementById("boost-rate").textContent=(counts.boost*20)+"%";
  }
  calc();
  return;
 }

 const ch=e.target.closest("[data-group]");
 if(ch){
  const g=ch.dataset.group;
  document.querySelectorAll(`[data-group="${g}"]`).forEach(x=>x.classList.remove("active"));
  ch.classList.add("active");

  if(g==="main"){
   mainBonus=Number(ch.dataset.value);
   document.getElementById("main-rate").textContent=mainBonus+"%";
  }else{
   friendBonus=Number(ch.dataset.value);
   document.getElementById("friend-rate").textContent=friendBonus+"%";
  }
  calc();
  return;
 }

 const b=e.target.closest(".bonus");
 if(b){
  b.classList.toggle("active");
  calc();
 }
});

calc();
