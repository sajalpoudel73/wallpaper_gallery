let currentWallpapers=[]
let currentIndex=0


function showGallery(){
document.getElementById("gallery-header").classList.remove("hidden")
document.getElementById("loading").classList.remove("hidden")
document.getElementById("gallery-container").classList.add("hidden")
document.getElementById("error").classList.add("hidden")
document.getElementById("about-page").classList.add("hidden")
loadAndDisplayWallpapers()
}


function showAbout(){
document.getElementById("gallery-header").classList.add("hidden")
document.getElementById("loading").classList.add("hidden")
document.getElementById("gallery-container").classList.add("hidden")
document.getElementById("error").classList.add("hidden")
document.getElementById("about-page").classList.remove("hidden")
}


function getWeekRange(date){

let start=new Date(date)
let end=new Date(date)

const day=start.getDay()

start.setDate(start.getDate()-day)
end.setDate(start.getDate()+6)

return {start,end}

}



function getGroupLabel(dateStr){

if(!dateStr) return "Undated"

const now=new Date()
const d=new Date(dateStr)

const sameMonth=
now.getFullYear()===d.getFullYear() &&
now.getMonth()===d.getMonth()

if(sameMonth){

let {start,end}=getWeekRange(d)

if(start.getMonth()!==d.getMonth())
start=new Date(d.getFullYear(),d.getMonth(),1)

if(end.getMonth()!==d.getMonth())
end=new Date(d.getFullYear(),d.getMonth()+1,0)

const startStr=start.toLocaleDateString('en-US',{month:'short',day:'numeric'})
const endStr=end.toLocaleDateString('en-US',{month:'short',day:'numeric'})

return `Week of ${startStr} – ${endStr}`

}

return d.toLocaleDateString('en-US',{
year:'numeric',
month:'long'
})

}



async function loadAndDisplayWallpapers(){

try{

const response=await fetch("wallpapers/database.json")

if(!response.ok) throw new Error()

const wallpapers=await response.json()

currentWallpapers=wallpapers

const grouped={}

wallpapers.forEach(w=>{

const date=new Date(w.date)
const label=getGroupLabel(w.date)

if(!grouped[label]){

grouped[label]={
wallpapers:[],
sortDate:date
}

}

grouped[label].wallpapers.push(w)

if(date>grouped[label].sortDate)
grouped[label].sortDate=date

})


const sortedGroups=Object.keys(grouped).sort((a,b)=>{

if(a==="Undated") return 1
if(b==="Undated") return -1

return grouped[b].sortDate-grouped[a].sortDate

})


const container=document.getElementById("gallery-container")

let html=""

let globalIndex=0

sortedGroups.forEach(group=>{

const items=grouped[group].wallpapers

html+=`

<section>

<div class="sticky top-0 z-10 bg-slate-950/90 backdrop-blur py-4 mb-6 flex items-center">

<h2 class="text-2xl font-semibold">${group}</h2>

<span class="ml-4 text-sm bg-blue-600 px-3 py-1 rounded-full">
${items.length}
</span>

</div>

<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">

`


items.forEach((w,i)=>{

html+=`

<div class="group cursor-pointer"
onclick="openModalByIndex(${globalIndex})">

<div class="relative rounded-xl overflow-hidden shadow-lg">

<div class="image-skeleton absolute inset-0"></div>

<img
src="${w.url}"
alt="${w.title}"
class="w-full h-52 object-cover transition duration-500 group-hover:scale-110"
onload="this.previousElementSibling.remove()"
loading="lazy"
/>

<div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent opacity-0 group-hover:opacity-100 transition flex items-end p-3">

<p class="text-sm text-white truncate">
${w.title}
</p>

</div>

</div>

</div>

`

globalIndex++

})

html+=`

</div>
</section>

`

})


container.innerHTML=html

document.getElementById("loading").classList.add("hidden")
container.classList.remove("hidden")

}

catch{

document.getElementById("loading").classList.add("hidden")
document.getElementById("error").classList.remove("hidden")

}

}



function openModalByIndex(index){

currentIndex=index

const wallpaper=currentWallpapers[index]

const modal=document.createElement("div")

modal.id="wallpaperModal"

modal.className="fixed inset-0 flex items-center justify-center z-50 p-6"

modal.innerHTML=`

<div id="ambient-bg"
class="absolute inset-0 transition duration-700"></div>

<div class="max-w-6xl w-full relative z-10">

<button
class="absolute -top-10 right-0 text-white text-3xl"
onclick="closeModal()"
>✕</button>

<div class="flex items-center justify-center gap-6">

<button
class="text-white text-4xl hover:text-blue-400 transition"
onclick="previousWallpaper()"
title="Previous (← Arrow Key)"
>
❮
</button>

<div class="flex-1">

<img
id="modalImage"
src="${wallpaper.url}"
class="w-full max-h-[85vh] object-contain rounded-xl shadow-2xl"
/>

</div>

<button
class="text-white text-4xl hover:text-blue-400 transition"
onclick="nextWallpaper()"
title="Next (→ Arrow Key)"
>
❯
</button>

</div>

<div class="mt-6 bg-black/60 backdrop-blur-md rounded-lg p-4">

<div class="flex justify-between items-start gap-4">

<div class="flex-1">

<h3 class="text-lg font-semibold text-white mb-2">
${wallpaper.title}
</h3>

<p class="text-sm text-gray-300 mb-3">
${new Date(wallpaper.date).toLocaleDateString('en-US', {year: 'numeric', month: 'long', day: 'numeric'})}
</p>

<p class="text-xs text-gray-400 leading-relaxed">
${wallpaper.copyright}
</p>

</div>

<a
href="${wallpaper.url}"
download
class="bg-blue-600 px-4 py-2 rounded hover:bg-blue-500 whitespace-nowrap flex-shrink-0"
>
Download
</a>

</div>

</div>

</div>

`

document.body.appendChild(modal)

generateAmbientColor(wallpaper.url)

document.addEventListener("keydown",keyboardNavigation)

}



function closeModal(){

const modal=document.getElementById("wallpaperModal")

if(modal) modal.remove()

document.removeEventListener("keydown",keyboardNavigation)

}



function keyboardNavigation(e){

if(e.key==="Escape") closeModal()

if(e.key==="ArrowRight"){

currentIndex++

if(currentIndex>=currentWallpapers.length)
currentIndex=0

reloadModal()

}

if(e.key==="ArrowLeft"){

currentIndex--

if(currentIndex<0)
currentIndex=currentWallpapers.length-1

reloadModal()

}

}



function reloadModal(){

const modal=document.getElementById("wallpaperModal")

if(!modal) return

const wallpaper=currentWallpapers[currentIndex]

const img=modal.querySelector("#modalImage")

img.src=wallpaper.url

const titleElement=modal.querySelector("h3")
titleElement.textContent=wallpaper.title

const dateElement=modal.querySelectorAll("p.text-gray-300")[0]
if(dateElement) dateElement.textContent=new Date(wallpaper.date).toLocaleDateString('en-US', {year: 'numeric', month: 'long', day: 'numeric'})

const copyrightElement=modal.querySelectorAll("p.text-gray-400")[0]
if(copyrightElement) copyrightElement.textContent=wallpaper.copyright

generateAmbientColor(wallpaper.url)

}


function nextWallpaper(){

currentIndex++

if(currentIndex>=currentWallpapers.length)
currentIndex=0

reloadModal()

}


function previousWallpaper(){

currentIndex--

if(currentIndex<0)
currentIndex=currentWallpapers.length-1

reloadModal()

}



function generateAmbientColor(url){

const img=new Image()

img.crossOrigin="Anonymous"

img.src=url

img.onload=()=>{

const canvas=document.createElement("canvas")

const ctx=canvas.getContext("2d")

canvas.width=50
canvas.height=50

ctx.drawImage(img,0,0,50,50)

const data=ctx.getImageData(0,0,50,50).data

let r=0,g=0,b=0,count=0

for(let i=0;i<data.length;i+=4){

r+=data[i]
g+=data[i+1]
b+=data[i+2]

count++

}

r=Math.floor(r/count)
g=Math.floor(g/count)
b=Math.floor(b/count)

const ambient=document.getElementById("ambient-bg")

ambient.style.background=`
radial-gradient(
circle at center,
rgba(${r},${g},${b},0.45),
#000 70%
)
`

}

}


document.addEventListener("DOMContentLoaded",showGallery)