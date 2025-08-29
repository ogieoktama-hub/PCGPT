import React from 'react'
export default function DatasetSelector({datasets, selected, onChange}){
  return (
    <div style={{marginBottom:12}}>
      <label style={{display:'block', marginBottom:6}}>Select Dataset</label>
      <select value={selected} onChange={e=>onChange(e.target.value)} style={{padding:8, width:'100%'}}>
        <option value='ALL'>All Datasets</option>
        {datasets.map((d,i)=> <option key={i} value={d}>{d}</option>)}
      </select>
    </div>
  )
}
