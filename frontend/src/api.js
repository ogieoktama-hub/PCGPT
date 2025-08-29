import axios from 'axios'
const API = axios.create({ baseURL: 'http://localhost:8000' })
export const getDatasets = ()=> API.get('/datasets')
export const ask = (q, dataset)=> API.get('/ask', { params: { q, dataset } })
