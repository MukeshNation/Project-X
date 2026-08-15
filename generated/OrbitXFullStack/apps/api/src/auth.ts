import {db} from './db.js';
export async function auth(req:any,res:any,next:any){const token=req.headers.authorization?.replace(/^Bearer\s+/i,'');if(!token)return res.status(401).json({error:'Login required'});const {data}=await db.auth.getUser(token);if(!data.user)return res.status(401).json({error:'Invalid session'});req.user=data.user;next()}
export async function admin(req:any,res:any,next:any){const {data}=await db.from('profiles').select('role').eq('id',req.user.id).single();if(data?.role!=='admin')return res.status(403).json({error:'Admin only'});next()}
