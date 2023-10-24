import { useState } from "react"

function HandleUrl() {
    const [url, setURL] = useState("");
    const [links, setLinks] = useState([]);
  
    function handleChange(e) {
      setURL(e.target.value)
    }

    async function sendUrl() {
      const response = await fetch('http://localhost:5555/get_url', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url:url})
      })
      if (response.status === 200) {
        const data = await response.json();
        setLinks(data)
      }
    }
  
    return (
      <div>
        <h2>Input Site URL</h2>
        <input
          value={url}
          onChange={handleChange}
          placeholder='URL'
          name='URL'
        />
        <button onClick={sendUrl}>Run</button>

        {links[0] && links.map(link => {
          return <p key={link}>{link}</p>
        })}
      </div>
    )
}

export default HandleUrl