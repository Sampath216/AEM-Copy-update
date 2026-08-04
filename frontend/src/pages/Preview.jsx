import { useState } from "react";
import api from "../services/api";

function Preview() {

    const [file, setFile] = useState(null);

    const [records, setRecords] = useState([]);

    const handlePreview = async () => {

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );

        const response =
            await api.post(
                "/update-preview",
                formData
            );

        setRecords(
            response.data
        );
    };

    return (

        <div style={{ padding: "20px" }}>

            <h1>
                Preview Changes
            </h1>

            <input
                type="file"
                onChange={(e) =>
                    setFile(
                        e.target.files[0]
                    )
                }
            />

            <br />
            <br />

            <button
                onClick={handlePreview}
            >
                Preview
            </button>

            <br />
            <br />

            <table border="1">

                <thead>

                    <tr>

                        <th>Page</th>

                        <th>Component</th>

                        <th>Property</th>

                        <th>Value</th>

                        <th>Status</th>

                    </tr>

                </thead>

                <tbody>

                {
                    records.map(
                        (record, index) => (

                        <tr key={index}>

                            <td>
                                {record.page_path}
                            </td>

                            <td>
                                {record.component}
                            </td>

                            <td>
                                {record.property}
                            </td>

                            <td>
                                {record.new_value}
                            </td>

                            <td>
                                {record.status}
                            </td>

                        </tr>

                    ))
                }

                </tbody>

            </table>

        </div>

    );
}

export default Preview;