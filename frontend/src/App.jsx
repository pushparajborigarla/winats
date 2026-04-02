import { useState } from "react";
import axios from "axios";
import { CircularProgressbar } from "react-circular-progressbar";

export default function App(){
  const [resume,setResume]=useState("");
  const [jd,setJD]=useState("");
  const [res,setRes]=useState(null);
  const [q,setQ]=useState("");
  const [ans,setAns]=useState("");

  const analyze=async()=>{
    const f=new FormData();
    f.append("resume",resume);
    f.append("jd",jd);
    const r=await axios.post("https://winats-1.onrender.com/analyze",f);
    setRes(r.data);
  }

  const chat=async()=>{
    const f=new FormData();
    f.append("resume",resume);
    f.append("jd",jd);
    f.append("question",q);
    const r=await axios.post("https://winats-1.onrender.com/chat",f);
    setAns(r.data.answer);
  }

  return(
    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",height:"100vh"}}>
      <div style={{padding:20}}>
        <h2>Input</h2>
        <textarea placeholder="Resume" onChange={e=>setResume(e.target.value)} style={{width:"100%",height:100}}/>
        <textarea placeholder="JD" onChange={e=>setJD(e.target.value)} style={{width:"100%",height:100}}/>
        <button onClick={analyze}>Analyze</button>
        <h3>Ask AI</h3>
        <input onChange={e=>setQ(e.target.value)} placeholder="Ask"/>
        <button onClick={chat}>Send</button>
        <p>{ans}</p>
      </div>

      <div style={{padding:20}}>
        <h2>Result</h2>
        {res && <>
          <div style={{width:120}}><CircularProgressbar value={res.score} text={res.score+"%"} /></div>
          <p>Missing: {res.must_missing.join(", ")}</p>
        </>}
      </div>
    </div>
  )
}
