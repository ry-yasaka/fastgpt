import React, { useState } from "react";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      console.log("111");
      console.log(username)
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username:username, 
          password:password}),
      });
      // console(response)
      if (response.ok) {
        // ログイン成功の処理
        console.log("login_OK");
        // setError("");
        // ログインが成功した場合に適切な処理を行う（例：トークンの保存など）
      } else {
        // ログイン失敗の処理
        const errorData = await response.json();
        setError(errorData.detail);
      }
    } catch (error) {
      console.error("Error:", error);
      setError("An error occurred");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
      {error && <p>{error}</p>}
    </div>
  );
}

export default Login;
