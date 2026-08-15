import json
import re
from pathlib import Path

from app.config import WORKSPACE
from core.full_stack_quality import FullStackQualityEngine


class FullStackBuilder:
    """Generate a deployable gaming SaaS starter without executing dependencies."""

    REQUIRED = [
        "README.md", "package.json", "docker-compose.yml",
        "apps/web/package.json", "apps/web/app/page.tsx",
        "apps/web/app/login/page.tsx", "apps/web/app/signup/page.tsx",
        "apps/web/app/games/page.tsx", "apps/web/app/leaderboard/page.tsx",
        "apps/web/app/profile/page.tsx", "apps/web/app/admin/page.tsx",
        "apps/api/package.json", "apps/api/src/index.ts",
        "apps/api/src/routes/payments.ts", "apps/api/src/routes/images.ts",
        "supabase/schema.sql",
    ]

    def _name(self, request: str):
        match = re.search(
            r"(?:called|named)\s+([A-Za-z][A-Za-z0-9_-]{1,30})(?=\s+(?:with|that|which|including|featuring|and)\b|[,.;]|$)",
            request,
            re.I,
        )
        brand = match.group(1).strip() if match else "NexusArena"
        safe = re.sub(r"[^A-Za-z0-9_-]", "", brand) or "NexusArena"
        return brand, f"{safe}FullStack"

    def _write(self, root: Path, relative: str, content: str):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip() + "\n", encoding="utf-8")

    def build(self, request: str):
        brand, folder = self._name(request)
        root = (WORKSPACE / folder).resolve()
        workspace = WORKSPACE.resolve()
        if workspace not in root.parents:
            raise ValueError("Unsafe full-stack project path.")
        root.mkdir(parents=True, exist_ok=True)

        files = self._files(brand, request)
        for relative, content in files.items():
            self._write(root, relative, content)

        # Autarch must deliver a complete product journey, not only a code
        # skeleton. The quality engine adds required account/support/legal
        # routes and shared authenticated navigation before validation.
        FullStackQualityEngine().enhance(root, brand, request)

        missing = [name for name in self.REQUIRED if not (root / name).exists()]
        if missing:
            raise RuntimeError(f"Missing full-stack files: {missing}")

        for manifest in self._manifests(root):
            json.loads(manifest.read_text(encoding="utf-8"))

        return {
            "project": str(root),
            "project_type": "fullstack-gaming",
            "status": "ready_for_install",
            "files": sorted(files),
            "features": [
                "Next.js React UI", "Node API", "Supabase/Postgres",
                "email auth", "player profiles", "leaderboard",
                "Socket.IO multiplayer", "admin game management",
                "Razorpay subscriptions", "AI image generation",
                "Docker and cloud deployment configs",
            ],
        }

    def validate(self, project_path: str, request: str = ""):
        root = Path(project_path).resolve()
        errors = [name for name in self.REQUIRED if not (root / name).exists()]
        checks = []
        for manifest in self._manifests(root):
            try:
                json.loads(manifest.read_text(encoding="utf-8"))
                checks.append(f"valid manifest: {manifest.relative_to(root)}")
            except Exception as error:
                errors.append(f"invalid {manifest.name}: {error}")
        schema = root / "supabase/schema.sql"
        if schema.exists():
            sql = schema.read_text(encoding="utf-8")
            for feature in ("profiles", "games", "leaderboard", "payments"):
                if not re.search(
                    rf"create\s+table\s+(?:if\s+not\s+exists\s+)?{feature}\s*\(",
                    sql,
                    re.IGNORECASE,
                ):
                    errors.append(f"schema missing {feature}")
        if not request:
            readme = (root / "README.md").read_text(encoding="utf-8", errors="ignore") if (root / "README.md").exists() else ""
            match = re.search(r"Original request:\s*(.+)", readme, re.S)
            request = match.group(1).strip() if match else ""
        quality = FullStackQualityEngine().audit(root, request)
        errors.extend(quality["errors"])
        checks.extend(f"quality warning: {warning}" for warning in quality["warnings"])
        return {
            "success": not errors,
            "project": str(root),
            "checks": checks,
            "errors": errors,
            "status": "validated" if not errors else "failed",
        }

    def _manifests(self, root: Path):
        return [
            root / "package.json",
            root / "apps/web/package.json",
            root / "apps/api/package.json",
        ]

    def _files(self, brand: str, request: str):
        root_package = {
            "name": re.sub(r"[^a-z0-9-]", "-", brand.lower()),
            "private": True,
            "workspaces": ["apps/*"],
            "scripts": {
                "dev": "concurrently \"npm run dev -w apps/api\" \"npm run dev -w apps/web\"",
                "build": "npm run build -w apps/api && npm run build -w apps/web",
                "start": "npm run start -w apps/api",
            },
            "devDependencies": {"concurrently": "^9.2.1"},
            "engines": {"node": "22.x"},
        }
        web_package = {
            "name": "web", "private": True, "scripts": {
                "dev": "next dev -p 3000", "build": "next build", "start": "next start -p 3000"
            },
            "dependencies": {
                "@supabase/supabase-js": "^2.57.0", "lucide-react": "^0.468.0",
                "next": "^15.5.0", "react": "^19.1.0", "react-dom": "^19.1.0",
                "socket.io-client": "^4.8.1"
            },
            "devDependencies": {"@types/node": "^22", "@types/react": "^19", "typescript": "^5.8.0"}
        }
        api_package = {
            "name": "api", "private": True, "type": "module", "scripts": {
                "dev": "tsx watch src/index.ts", "build": "tsc", "start": "node dist/index.js"
            },
            "dependencies": {
                "@supabase/supabase-js": "^2.57.0", "cors": "^2.8.5", "dotenv": "^16.4.7",
                "express": "^5.1.0", "openai": "^5.19.0", "razorpay": "^2.9.6", "socket.io": "^4.8.1"
            },
            "devDependencies": {"@types/cors": "^2.8.17", "@types/express": "^5", "@types/node": "^22", "tsx": "^4.20.0", "typescript": "^5.8.0"}
        }

        return {
            "package.json": json.dumps(root_package, indent=2),
            ".gitignore": "node_modules\n.next\ndist\n.env\n.env.local\ncoverage\n",
            ".env.example": "SUPABASE_URL=\nSUPABASE_SERVICE_ROLE_KEY=\nRAZORPAY_KEY_ID=\nRAZORPAY_KEY_SECRET=\nRAZORPAY_PRO_PLAN_ID=\nRAZORPAY_BUSINESS_PLAN_ID=\nOPENAI_API_KEY=\nWEB_URL=http://localhost:3000\nPORT=4000\n",
            "README.md": f"""# {brand}

Generated by Autarch Full-Stack Builder.

## Stack
- Next.js + React frontend
- Express + Socket.IO API
- Supabase Auth + Postgres + Row Level Security
- Razorpay subscriptions
- Configurable AI image generation
- Docker deployment

## Start
1. Copy `.env.example` to `.env` and `apps/web/.env.local.example` to `apps/web/.env.local`.
2. Run `supabase/schema.sql` in the Supabase SQL editor.
3. Run `npm install` and `npm run dev`.
4. Configure Razorpay webhooks to `/api/payments/webhook`.

Original request: {request[:500]}
""",
            "docker-compose.yml": """services:
  api:
    build: { context: ., dockerfile: apps/api/Dockerfile }
    env_file: .env
    ports: [\"4000:4000\"]
  web:
    build: { context: ., dockerfile: apps/web/Dockerfile }
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:4000
    ports: [\"3000:3000\"]
    depends_on: [api]
""",
            "render.yaml": """services:
  - type: web
    name: gaming-api
    runtime: docker
    dockerfilePath: ./apps/api/Dockerfile
    healthCheckPath: /api/health
  - type: web
    name: gaming-web
    runtime: docker
    dockerfilePath: ./apps/web/Dockerfile
""",
            "apps/web/package.json": json.dumps(web_package, indent=2),
            "apps/web/tsconfig.json": json.dumps({"compilerOptions": {"target": "ES2020", "lib": ["dom", "esnext"], "strict": True, "noEmit": True, "module": "esnext", "moduleResolution": "bundler", "jsx": "preserve", "plugins": [{"name": "next"}]}, "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"]}, indent=2),
            "apps/web/next.config.ts": "const config = { output: 'standalone' }; export default config;",
            "apps/web/.env.local.example": "NEXT_PUBLIC_SUPABASE_URL=\nNEXT_PUBLIC_SUPABASE_ANON_KEY=\nNEXT_PUBLIC_API_URL=http://localhost:4000\n",
            "apps/web/Dockerfile": """FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
COPY apps/web/package.json apps/web/package.json
COPY apps/api/package.json apps/api/package.json
RUN npm install
COPY apps/web apps/web
RUN npm run build -w apps/web
FROM node:22-alpine
WORKDIR /app
COPY --from=build /app/apps/web/.next/standalone ./
COPY --from=build /app/apps/web/.next/static ./apps/web/.next/static
EXPOSE 3000
CMD [\"node\", \"apps/web/server.js\"]
""",
            "apps/web/lib/supabase.ts": """import { createClient } from '@supabase/supabase-js';
const url = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co';
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-anon-key';
export const supabase = createClient(url, anonKey);
""",
            "apps/web/lib/api.ts": "export const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';\n",
            "apps/web/app/layout.tsx": f"""import './globals.css';
import Link from 'next/link';
export const metadata = {{ title: '{brand}', description: 'Competitive gaming, tournaments and community' }};
export default function Layout({{children}}:{{children:React.ReactNode}}){{return <html lang=\"en\"><body><nav><Link className=\"brand\" href=\"/\">{brand}</Link><div><Link href=\"/games\">Games</Link><Link href=\"/leaderboard\">Leaderboard</Link><Link href=\"/profile\">Profile</Link><Link href=\"/pricing\">Pricing</Link><Link href=\"/admin\">Admin</Link></div></nav>{{children}}<footer>© 2026 {brand} · Built with Autarch AI</footer></body></html>}}
""",
            "apps/web/app/globals.css": self._css(),
            "apps/web/app/page.tsx": f"""import Link from 'next/link';
const games=[['NEON STRIKE','Tactical 5v5 arena','⚡'],['VOID RACERS','Interstellar racing','◈'],['KINGDOM SIEGE','Massive strategy battles','♜']];
export default function Home(){{return <main><section className=\"hero\"><span className=\"pill\">LIVE COMPETITIVE GAMING</span><h1>PLAY. COMPETE.<br/><em>BECOME LEGEND.</em></h1><p>Discover games, join live rooms, climb the leaderboard and compete in community tournaments.</p><div className=\"actions\"><Link className=\"primary\" href=\"/signup\">Create player</Link><Link className=\"secondary\" href=\"/games\">Explore games</Link></div></section><section><div className=\"sectionHead\"><h2>Featured games</h2><Link href=\"/games\">View all →</Link></div><div className=\"grid\">{{games.map(([name,text,icon])=><article className=\"game\" key={{name}}><div className=\"cover\">{{icon}}</div><h3>{{name}}</h3><p>{{text}}</p><button>Play now</button></article>)}}</div></section></main>}}
""",
            "apps/web/app/games/page.tsx": """'use client'; import {useEffect,useState} from 'react'; import {API} from '../../lib/api';
export default function Games(){const [games,setGames]=useState<any[]>([]);useEffect(()=>{fetch(`${API}/api/games`).then(r=>r.json()).then(d=>setGames(d.games||[]))},[]);return <main><h1>Game library</h1><div className="grid">{games.map(g=><article className="game" key={g.id}><div className="cover">🎮</div><h3>{g.title}</h3><p>{g.description}</p><button>Join game</button></article>)}</div></main>}
""",
            "apps/web/app/leaderboard/page.tsx": """'use client'; import {useEffect,useState} from 'react'; import {API} from '../../lib/api';
export default function Leaderboard(){const [rows,setRows]=useState<any[]>([]);useEffect(()=>{fetch(`${API}/api/leaderboard`).then(r=>r.json()).then(d=>setRows(d.players||[]))},[]);return <main><h1>Global leaderboard</h1><div className="panel">{rows.map((p,i)=><div className="row" key={p.id}><b>#{i+1}</b><span>{p.username}</span><strong>{p.score} XP</strong></div>)}</div></main>}
""",
            "apps/web/app/profile/page.tsx": """'use client'; import {useEffect,useState} from 'react'; import {supabase} from '../../lib/supabase';
export default function Profile(){const [user,setUser]=useState<any>();useEffect(()=>{supabase.auth.getUser().then(({data})=>setUser(data.user))},[]);return <main><h1>Player profile</h1><div className="panel"><p>{user?.email||'Sign in to view your profile.'}</p><p>Manage your gamer tag, avatar and connected account.</p></div></main>}
""",
            "apps/web/app/admin/page.tsx": """'use client'; import {useEffect,useState} from 'react'; import {API} from '../../lib/api'; import {supabase} from '../../lib/supabase';
export default function Admin(){const [data,setData]=useState<any>();useEffect(()=>{supabase.auth.getSession().then(({data:s})=>fetch(`${API}/api/admin`,{headers:{Authorization:`Bearer ${s.session?.access_token}`}}).then(r=>r.json()).then(setData))},[]);return <main><h1>Game management</h1><div className="stats"><article>Players <b>{data?.players||0}</b></article><article>Games <b>{data?.games||0}</b></article><article>Revenue <b>₹{(data?.revenue||0)/100}</b></article></div><div className="panel">Admin-only game, tournament and player controls.</div></main>}
""",
            "apps/web/app/pricing/page.tsx": """export default function Pricing(){return <main><h1>Choose your rank</h1><div className="grid"><article className="game"><h2>Free</h2><h3>₹0</h3><p>Public games and leaderboards</p></article><article className="game featured"><h2>Pro</h2><h3>₹499/mo</h3><p>Tournaments, premium rooms and rewards</p></article><article className="game"><h2>Squad</h2><h3>₹1,499/mo</h3><p>Team management and private servers</p></article></div></main>}
""",
            "apps/web/app/login/page.tsx": self._auth_page("Login", "signInWithPassword"),
            "apps/web/app/signup/page.tsx": self._auth_page("Create account", "signUp"),
            "apps/api/package.json": json.dumps(api_package, indent=2),
            "apps/api/tsconfig.json": json.dumps({"compilerOptions": {"target": "ES2022", "module": "NodeNext", "moduleResolution": "NodeNext", "outDir": "dist", "strict": True, "esModuleInterop": True}, "include": ["src/**/*.ts"]}, indent=2),
            "apps/api/Dockerfile": """FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
COPY apps/api/package.json apps/api/package.json
COPY apps/web/package.json apps/web/package.json
RUN npm install
COPY apps/api apps/api
RUN npm run build -w apps/api
EXPOSE 4000
CMD [\"node\", \"apps/api/dist/index.js\"]
""",
            "apps/api/src/db.ts": """import {createClient} from '@supabase/supabase-js';
export const db=createClient(process.env.SUPABASE_URL!,process.env.SUPABASE_SERVICE_ROLE_KEY!,{auth:{persistSession:false}});
""",
            "apps/api/src/auth.ts": """import {db} from './db.js';
export async function auth(req:any,res:any,next:any){const token=req.headers.authorization?.replace(/^Bearer\\s+/i,'');if(!token)return res.status(401).json({error:'Login required'});const {data}=await db.auth.getUser(token);if(!data.user)return res.status(401).json({error:'Invalid session'});req.user=data.user;next()}
export async function admin(req:any,res:any,next:any){const {data}=await db.from('profiles').select('role').eq('id',req.user.id).single();if(data?.role!=='admin')return res.status(403).json({error:'Admin only'});next()}
""",
            "apps/api/src/index.ts": self._api_index(),
            "apps/api/src/routes/payments.ts": self._payments_route(),
            "apps/api/src/routes/images.ts": self._images_route(),
            "supabase/schema.sql": self._schema(),
        }

    def _auth_page(self, title: str, method: str):
        action = "supabase.auth.signInWithPassword({email,password})" if method == "signInWithPassword" else "supabase.auth.signUp({email,password,options:{data:{username}}})"
        return f"""'use client'; import {{FormEvent,useState}} from 'react'; import {{supabase}} from '../../lib/supabase';
export default function Auth(){{const [email,setEmail]=useState(''),[password,setPassword]=useState(''),[username,setUsername]=useState(''),[message,setMessage]=useState('');async function submit(e:FormEvent){{e.preventDefault();const {{error}}=await {action};setMessage(error?.message||'Success — check your email if confirmation is enabled.')}}return <main><form className=\"auth\" onSubmit={{submit}}><h1>{title}</h1>{title.startswith('Create') and '<input placeholder="Gamer tag" value={username} onChange={e=>setUsername(e.target.value)}/>' or ''}<input type=\"email\" placeholder=\"Email\" value={{email}} onChange={{e=>setEmail(e.target.value)}}/><input type=\"password\" placeholder=\"Password\" value={{password}} onChange={{e=>setPassword(e.target.value)}}/><button>Continue</button><p>{{message}}</p></form></main>}}
"""

    def _api_index(self):
        return """import 'dotenv/config'; import express from 'express'; import cors from 'cors'; import {createServer} from 'http'; import {Server} from 'socket.io'; import {db} from './db.js'; import {auth,admin} from './auth.js'; import payments from './routes/payments.js'; import images from './routes/images.js';
const app=express(),http=createServer(app),io=new Server(http,{cors:{origin:process.env.WEB_URL}});app.use(cors({origin:process.env.WEB_URL}));app.use('/api/payments/webhook',express.raw({type:'application/json'}));app.use(express.json());
app.get('/api/health',(_,res)=>res.json({ok:true}));app.get('/api/games',async(_,res)=>{const {data,error}=await db.from('games').select('*').eq('published',true);res.status(error?500:200).json(error?{error:error.message}:{games:data})});app.get('/api/leaderboard',async(_,res)=>{const {data,error}=await db.from('leaderboard').select('*').order('score',{ascending:false}).limit(100);res.status(error?500:200).json(error?{error:error.message}:{players:data})});
app.get('/api/admin',auth,admin,async(_req,res)=>{const [p,g,pay]=await Promise.all([db.from('profiles').select('*',{count:'exact',head:true}),db.from('games').select('*',{count:'exact',head:true}),db.from('payments').select('amount').eq('status','captured')]);res.json({players:p.count,games:g.count,revenue:(pay.data||[]).reduce((s,x)=>s+x.amount,0)})});app.use('/api/payments',payments);app.use('/api/images',auth,images);
const rooms=new Map<string,Map<string,{x:number,y:number}>>();io.on('connection',socket=>{socket.on('room:join',(room:string)=>{socket.join(room);if(!rooms.has(room))rooms.set(room,new Map());rooms.get(room)!.set(socket.id,{x:0,y:0});io.to(room).emit('room:state',Object.fromEntries(rooms.get(room)!))});socket.on('player:move',({room,x,y})=>{rooms.get(room)?.set(socket.id,{x,y});socket.to(room).emit('player:moved',{id:socket.id,x,y})});socket.on('disconnect',()=>rooms.forEach((players,room)=>{players.delete(socket.id);io.to(room).emit('player:left',socket.id)}))});
http.listen(Number(process.env.PORT)||4000,()=>console.log('Gaming API ready'));
"""

    def _payments_route(self):
        return """import {Router} from 'express';import crypto from 'crypto';import Razorpay from 'razorpay';import {auth} from '../auth.js';import {db} from '../db.js';const r=Router();const client=()=>new Razorpay({key_id:process.env.RAZORPAY_KEY_ID!,key_secret:process.env.RAZORPAY_KEY_SECRET!});
r.post('/subscribe',auth,async(req:any,res)=>{const plan=req.body.plan==='business'?'business':'pro';const plan_id=plan==='pro'?process.env.RAZORPAY_PRO_PLAN_ID:process.env.RAZORPAY_BUSINESS_PLAN_ID;const subscription=await client().subscriptions.create({plan_id:plan_id!,total_count:12,customer_notify:1,notes:{user_id:req.user.id,plan}});res.json({subscription,keyId:process.env.RAZORPAY_KEY_ID})});
r.post('/webhook',async(req,res)=>{const signature=String(req.headers['x-razorpay-signature']||'');const expected=crypto.createHmac('sha256',process.env.RAZORPAY_KEY_SECRET!).update(req.body).digest('hex');if(signature.length!==expected.length||!crypto.timingSafeEqual(Buffer.from(signature),Buffer.from(expected)))return res.status(400).send('Invalid signature');const event=JSON.parse(req.body.toString());if(event.event==='payment.captured'){const p=event.payload.payment.entity;await db.from('payments').upsert({user_id:p.notes.user_id,plan:p.notes.plan,amount:p.amount,currency:p.currency,status:p.status,provider_payment_id:p.id},{onConflict:'provider_payment_id'})}res.json({ok:true})});export default r;
"""

    def _images_route(self):
        return """import {Router} from 'express';import OpenAI from 'openai';const r=Router();r.post('/generate',async(req,res)=>{if(!process.env.OPENAI_API_KEY)return res.status(503).json({error:'Image provider not configured'});const ai=new OpenAI({apiKey:process.env.OPENAI_API_KEY});const image=await ai.images.generate({model:'gpt-image-1',prompt:String(req.body.prompt).slice(0,1000),size:'1024x1024'});res.json({image:image.data?.[0]})});export default r;
"""

    def _schema(self):
        return """create extension if not exists pgcrypto;
create table if not exists profiles(id uuid primary key references auth.users on delete cascade,username text unique,avatar_url text,role text not null default 'player' check(role in('player','admin')),plan text not null default 'free',created_at timestamptz default now());
create table if not exists games(id uuid primary key default gen_random_uuid(),title text not null,slug text unique not null,description text,cover_url text,published boolean default false,created_at timestamptz default now());
create table if not exists leaderboard(id uuid primary key default gen_random_uuid(),user_id uuid unique references profiles on delete cascade,username text not null,score bigint default 0,wins integer default 0,updated_at timestamptz default now());
create table if not exists payments(id uuid primary key default gen_random_uuid(),user_id uuid references profiles,plan text,amount integer not null,currency text default 'INR',status text,provider_payment_id text unique,created_at timestamptz default now());
alter table profiles enable row level security;alter table games enable row level security;alter table leaderboard enable row level security;alter table payments enable row level security;
create policy "profiles public read" on profiles for select using(true);create policy "profile own update" on profiles for update using(auth.uid()=id);create policy "games public read" on games for select using(published=true);create policy "leaderboard public read" on leaderboard for select using(true);
create or replace function new_player() returns trigger language plpgsql security definer set search_path=public as $$begin insert into profiles(id,username) values(new.id,coalesce(new.raw_user_meta_data->>'username',split_part(new.email,'@',1)));insert into leaderboard(user_id,username) values(new.id,coalesce(new.raw_user_meta_data->>'username',split_part(new.email,'@',1)));return new;end;$$;drop trigger if exists auth_player on auth.users;create trigger auth_player after insert on auth.users for each row execute procedure new_player();
insert into games(title,slug,description,published) values('Neon Strike','neon-strike','Tactical competitive arena',true),('Void Racers','void-racers','Interstellar racing league',true),('Kingdom Siege','kingdom-siege','Massive strategy battles',true) on conflict do nothing;
"""

    def _css(self):
        return """*{box-sizing:border-box}body{margin:0;background:#070813;color:#f5f7ff;font-family:Inter,system-ui}nav{height:72px;padding:0 6%;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #24263b;background:#090b16dd;position:sticky;top:0;z-index:3;backdrop-filter:blur(16px)}nav a{color:#aeb4ca;text-decoration:none;margin-left:24px}.brand{color:#fff!important;font-weight:900;letter-spacing:.12em;margin:0}.hero{min-height:72vh;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;background:radial-gradient(circle at 75% 40%,#6325d855,transparent 35%);padding:8%}.hero h1{font-size:clamp(3rem,8vw,7rem);line-height:.9;margin:24px 0}.hero em{font-style:normal;color:#8c6cff}.hero p{max-width:620px;color:#aab0c4;font-size:1.15rem;line-height:1.7}.pill{border:1px solid #5946a8;border-radius:99px;padding:8px 12px;color:#b7a8ff}.actions{display:flex;gap:12px;margin-top:22px}.primary,.secondary,button{padding:12px 18px;border-radius:10px;border:0;font-weight:800;cursor:pointer}.primary,button{background:linear-gradient(135deg,#805bff,#516cff);color:#fff}.secondary{border:1px solid #353853;color:#fff}main{min-height:calc(100vh - 140px);padding:5% 7%}section{margin-bottom:90px}.sectionHead{display:flex;justify-content:space-between;align-items:center}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}.game,.panel,.stats article{background:#111424;border:1px solid #292d46;border-radius:18px;padding:22px}.game.featured{border-color:#785dff;box-shadow:0 0 50px #6847ff22}.cover{height:170px;border-radius:13px;background:linear-gradient(135deg,#342273,#142342);display:grid;place-items:center;font-size:4rem}.game p{color:#979eb5}.row{display:grid;grid-template-columns:70px 1fr auto;padding:16px;border-bottom:1px solid #292d46}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin:25px 0}.stats b{display:block;font-size:2rem;margin-top:10px}.auth{max-width:430px;margin:6vh auto;background:#111424;padding:30px;border:1px solid #292d46;border-radius:18px}.auth input{width:100%;padding:13px;margin:8px 0;background:#090b15;color:white;border:1px solid #343854;border-radius:9px}.auth button{width:100%;margin-top:12px}footer{text-align:center;padding:30px;color:#687087;border-top:1px solid #24263b}@media(max-width:700px){nav div{display:none}.hero{padding:12% 7%}.stats{grid-template-columns:1fr}}
"""
