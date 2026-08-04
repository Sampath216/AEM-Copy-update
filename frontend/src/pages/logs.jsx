import { useEffect, useState } from "react";
import api from "../services/api";

function Logs() {

    const [logs, setLogs] = useState([]);

    useEffect(() => {
        fetchLogs();
    }, []);

    const fetchLogs = async () => {

        try {

            const response =
                await api.get("/logs");

            setLogs(response.data);

        } catch (error) {

            console.error(error);

        }
    };

    return (
        <div style={{ padding: "20px" }}>

            <h1>Execution Logs</h1>

            <table border="1" cellPadding="10">

                <thead>
                    <tr>
                        <th>ID</th>
                        <th>File Name</th>
                        <th>Total Rows</th>
                        <th>Valid Rows</th>
                        <th>Error Count</th>
                    </tr>
                </thead>

                <tbody>

                    {logs.map(log => (

                        <tr key={log.id}>

                            <td>{log.id}</td>

                            <td>{log.filename}</td>

                            <td>{log.total_rows}</td>

                            <td>{log.valid_rows}</td>

                            <td>{log.error_count}</td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </div>
    );
}

export default Logs;