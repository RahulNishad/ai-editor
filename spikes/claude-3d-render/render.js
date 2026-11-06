const {chromium}=require('playwright'); const http=require('http'); const fs=require('fs'); const path=require('path');
const root=__dirname, FPS=30, DUR=6, FRAMES=FPS*DUR;
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript'};
const srv=http.createServer((req,res)=>{const p=path.join(root,decodeURIComponent(req.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){res.writeHead(404);return res.end();}res.writeHead(200,{'content-type':mime[path.extname(p)]||'application/octet-stream'});res.end(d);});});
(async()=>{
  await new Promise(r=>srv.listen(0,'127.0.0.1',r)); const port=srv.address().port;
  const browser=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const page=await browser.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
  page.on('pageerror',e=>console.error('PAGEERROR',e.message)); page.on('console',m=>{if(m.type()==='error')console.error('CONSOLE',m.text());});
  await page.goto(`http://127.0.0.1:${port}/scene.html`); await page.waitForFunction(()=>window.__ready===true,null,{timeout:30000});
  const t0=Date.now();
  for(let f=0;f<FRAMES;f++){ await page.evaluate(f=>window.renderFrame(f),f); await page.screenshot({path:path.join(root,'frames',String(f).padStart(4,'0')+'.png'),type:'png'}); if(f%30===0) console.log('frame',f,((Date.now()-t0)/1000).toFixed(1)+'s'); }
  console.log('done', FRAMES, 'frames in', ((Date.now()-t0)/1000).toFixed(1)+'s');
  await browser.close(); srv.close();
})().catch(e=>{console.error(e);process.exit(1);});
