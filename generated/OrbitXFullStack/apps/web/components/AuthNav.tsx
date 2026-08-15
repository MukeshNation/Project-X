"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "../lib/supabase";
export default function AuthNav() {
  const [email,setEmail]=useState(""); const router=useRouter();
  useEffect(()=>{supabase.auth.getSession().then(({data})=>setEmail(data.session?.user.email||""));const {data}=supabase.auth.onAuthStateChange((_e,s)=>setEmail(s?.user.email||""));return()=>data.subscription.unsubscribe()},[]);
  async function logout(){await supabase.auth.signOut();setEmail("");router.push("/");router.refresh()}
  return <nav><Link className="brand" href="/">OrbitX</Link><div><Link href="/games">Games</Link><Link href="/leaderboard">Leaderboard</Link><Link href="/pricing">Pricing</Link><Link href="/help">Help</Link>{email?<><Link href="/profile">Profile</Link><button className="navLogout" onClick={logout}>Log out</button></>:<><Link href="/login">Log in</Link><Link className="navJoin" href="/signup">Join free</Link></>}</div></nav>
}
