// usage: node render.js <from> <to> [stride]   (frames, inclusive-exclusive)
const {chromium}=require('playwright'),http=require('http'),fs=require('fs'),path=require('path');
const root=__dirname,[from,to,stride=1]=process.argv.slice(2).map(Number);
const mime={'.html':'text/html','.js':'text/javascript','.json':'application/json','.woff2':'font/woff2'};
const srv=http.createServer((q,r)=>{const p=path.join(root,decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);return r.end();}r.writeHead(200,{'content-type':mime[path.extname(p)]||'application/octet-stream'});r.end(d);});});
(async()=>{await new Promise(r=>srv.listen(0,'127.0.0.1',r));
 const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
 const pg=await b.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
 pg.on('pageerror',e=>console.error('PAGEERROR',e.message));pg.on('console',m=>{if(m.type()==='error')console.error('CONSOLE',m.text());});
 await pg.goto(`http://127.0.0.1:${srv.address().port}/comp.html`);await pg.waitForFunction(()=>window.__ready===true,null,{timeout:120000});
 fs.mkdirSync(path.join(root,'frames'),{recursive:true});const t0=Date.now();
 for(let f=from;f<to;f+=stride){await pg.evaluate(f=>window.renderFrame(f),f);await pg.screenshot({path:path.join(root,'frames',String(f).padStart(5,'0')+'.jpg'),type:'jpeg',quality:92});
   if((f-from)%(150*stride)===0)console.log(`[${from}-${to}] frame ${f} ${((Date.now()-t0)/1000).toFixed(0)}s`);}
 console.log(`[${from}-${to}] done in ${((Date.now()-t0)/1000).toFixed(0)}s`);await b.close();srv.close();})().catch(e=>{console.error(e);process.exit(1);});
