import React, {useEffect, useState} from 'react'
import DatasetSelector from './components/DatasetSelector'
import { getDatasets, ask } from './api'
export default function App(){
  const [datasets, setDatasets] = useState([])
  const [selected, setSelected] = useState('ALL')
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  useEffect(()=>{ getDatasets().then(r=>{ setDatasets(r.data.datasets) }) },[])
  const doAsk = async ()=>{
    if(!query) return
    const r = await ask(query, selected)
    setResults(r.data.results)
  }
  return (
    <div style={{padding:20, maxWidth:900, margin:'auto'}}>
      <h1>ChatGPT Prototype — Multi Dataset</h1>
      <DatasetSelector datasets={datasets} selected={selected} onChange={setSelected} />
      <input style={{width:'100%', padding:10}} value={query} onChange={e=>setQuery(e.target.value)} placeholder='Ask something about your data...' />
      <button style={{marginTop:10}} onClick={doAsk}>Ask</button>
      <div style={{marginTop:20}}>
        {results.map((r,i)=> (
          <div key={i} style={{border:'1px solid #ddd', padding:10, marginBottom:8}}>
            <div style={{fontSize:12, color:'#666'}}>Dataset: {r.collection} — score: {r.score.toFixed(4)}</div>
            <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(r.payload, null, 2)}</pre>
          </div>
        ))}
      </div>
    </div>
  )
}
