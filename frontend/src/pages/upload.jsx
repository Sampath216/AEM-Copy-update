import { useState } from "react";
import api from "../services/api";

function Upload() {

  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {

    if (!file) {
      alert("Select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {

      const response =
        await api.post(
          "/upload",
          formData
        );

      setResult(response.data);

    } catch (error) {

      console.error(error);

      alert(
        "Upload Failed"
      );
    }
  };

  return (
    <div style={{ padding: "20px" }}>

      <h1>
        Author Automation Portal
      </h1>

      <input
        type="file"
        onChange={(e) =>
          setFile(
            e.target.files[0]
          )
        }
      />

      <br /><br />

      <button onClick={handleUpload}>
        Upload
      </button>

      {
        result && (

          <div>

            <h3>
              Validation Result
            </h3>

            <p>
              Total Rows:
              {result.total_rows}
            </p>

            <p>
              Valid Rows:
              {result.valid_rows}
            </p>

            <p>
              Errors:
              {result.error_count}
            </p>

          </div>

        )
      }

    </div>
  );
}

export default Upload;