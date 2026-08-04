import { useState } from "react";
import api from "../services/api";

function Execute() {

    const [file, setFile] = useState(null);

    const [report, setReport] = useState(null);

    const handleExecute = async () => {

        if (!file) {
            alert("Select Excel File");
            return;
        }

        const formData = new FormData();

        formData.append(
            "file",
            file
        );

        try {

            const response =
                await api.post(
                    "/execute-update",
                    formData
                );

            setReport(
                response.data
            );

        } catch (error) {

            console.error(error);

            alert(
                "Execution Failed"
            );
        }
    };

    return (

        <div style={{ padding: "20px" }}>

            <h1>
                Execute Component Updates
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
                onClick={handleExecute}
            >
                Execute Update
            </button>

            {
                report && (

                    <div>

                        <h2>
                            Execution Report
                        </h2>

                        <p>
                            Total Records:
                            {report.total_records}
                        </p>

                        <p>
                            Success Count:
                            {report.success_count}
                        </p>

                        <p>
                            Failed Count:
                            {report.failed_count}
                        </p>

                    </div>

                )
            }

        </div>
    );
}

export default Execute;