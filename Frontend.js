import React, { useState } from 'react';

function App() {
  const [phone, setPhone] = useState('');
  const [amount, setAmount] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    setMessage("Processing...");

    const res = await fetch('https://YOUR_BACKEND_URL.onrender.com/stkpush', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone,
        amount,
        callback_url: 'https://webhook.site/your-unique-url'
      })
    });
    const data = await res.json();
    setMessage(JSON.stringify(data));
  };

  return (
    <div style={{maxWidth: 400, margin: "50px auto"}}>
      <h2>M-Pesa STK Push Test</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Phone (e.g. 254708374149):</label>
          <input value={phone} onChange={e=>setPhone(e.target.value)} required />
        </div>
        <div>
          <label>Amount:</label>
          <input type="number" value={amount} onChange={e=>setAmount(e.target.value)} required />
        </div>
        <button type="submit">Pay</button>
      </form>
      <pre>{message}</pre>
    </div>
  );
}

export default App;