import { useState } from "react"

function HandleUrl() {
    const [url, setURL] = useState("");
  
    function handleChange(e) {
      setURL(e.target.value)
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
        <button onClick={() => console.log("click")}>Run</button>
      </div>
    )
}

export default HandleUrl