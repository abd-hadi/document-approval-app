import { useState } from 'react';

export default function App() {
  const [backendUrl, setBackendUrl] = useState('http://44.195.62.201:8000');
  const [uploadedBy, setUploadedBy] = useState('zoraiz');
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState('');

  const uploadDocument = async () => {
    if (!file) {
      setResult('Please select a file first');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('uploadedBy', uploadedBy);

    const res = await fetch(`${backendUrl}/documents`, {
      method: 'POST',
      body: formData,
    });

    const data = await res.json();
    setResult(JSON.stringify(data, null, 2));
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial' }}>
      <h1>Document Approval Workflow</h1>

      <p>Upload a document for approval.</p>

      <input
        style={{ width: '400px', padding: '8px', marginBottom: '10px' }}
        value={backendUrl}
        onChange={(e) => setBackendUrl(e.target.value)}
        placeholder="Backend API URL"
      />
      <br />

      <input
        style={{ width: '400px', padding: '8px', marginBottom: '10px' }}
        value={uploadedBy}
        onChange={(e) => setUploadedBy(e.target.value)}
        placeholder="Uploaded By"
      />
      <br />

      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <br /><br />

      <button onClick={uploadDocument} style={{ padding: '10px 20px' }}>
        Upload Document
      </button>

      <pre style={{ marginTop: '20px', background: '#eee', padding: '15px' }}>
        {result}
      </pre>
    </div>
  );
}
