'use client'

import { useState } from 'react'

export default function Home() {
  const [form, setForm] = useState({
    OverallQual: 7,
    GrLivArea: 1500,
    GarageCars: 2,
    TotalBsmtSF: 800,
    FullBath: 2,
    YearBuilt: 2005
  })

  const [price, setPrice] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e: any) => {
    setForm({ ...form, [e.target.name]: Number(e.target.value) })
  }

  const predictPrice = async () => {
    if (form.GrLivArea < 300 || form.GrLivArea > 5000) {
      alert("Enter valid area (300–5000)")
      return
    }

    try {
      setLoading(true)

      const res = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      })

      const data = await res.json()
      setPrice(data.predicted_price)
    } catch (error) {
      alert("API not connected")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
      <div className="bg-white p-6 rounded-xl shadow-lg w-[350px]">
      <p className="text-center text-gray-600 text-sm mb-3">
  Enter house details to estimate price using ML
</p>
        <h1 className="text-xl font-bold text-center mb-4">
          🏠 House Price Predictor
          <p className="text-xs text-center mt-4 text-gray-500">
  Built by Kishor 🚀
</p>
        </h1>

        {Object.keys(form).map((key) => (
          <div key={key} className="mb-2">
            <label className="text-sm font-semibold">{key}</label>
            <input
              type="number"
              name={key}
              value={(form as any)[key]}
              onChange={handleChange}
              className="w-full p-2 border rounded"
            />
          </div>
        ))}

        <button
          onClick={predictPrice}
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded mt-3"
        >
          {loading ? "Predicting..." : "Predict Price"}
        </button>
        

        {price !== null && (
          <h2 className="text-center mt-4 text-green-600 font-bold">
            💰 ₹{price.toLocaleString('en-IN')}
          </h2>
          
        )}

      </div>
    </div>
  )
}