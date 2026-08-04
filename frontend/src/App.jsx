import {
 BrowserRouter,
 Routes,
 Route,
 Link
}
from "react-router-dom";

import Upload from "./pages/Upload";
import Logs from "./pages/Logs";
import Preview from "./pages/Preview";
import Execute from "./pages/Execute";

function App() {

 return (

 <BrowserRouter>

    <div
      style={{
        padding: "10px"
      }}
    >

      <Link to="/">
        Upload
      </Link>

      {" | "}

      <Link to="/logs">
        Logs
      </Link>

      {" | "}

      <Link to="/preview">
        Preview
      </Link>

      {" | "}

      <Link to="/execute">
        Execute
      </Link>

    </div>

    <Routes>

      <Route
        path="/"
        element={<Upload />}
      />

      <Route
        path="/logs"
        element={<Logs />}
      />

      <Route
        path="/preview"
        element={<Preview />}
      />

      <Route
        path="/execute"
        element={<Execute />}
      />

    </Routes>

 </BrowserRouter>

 );

}

export default App;