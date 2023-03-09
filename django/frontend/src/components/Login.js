import React, { useState } from 'react';
import './Login.css';
import PropTypes from 'prop-types';
import { useHistory } from "react-router-dom";

async function loginUser(credentials) {
    return fetch('http://localhost:8000/api/v1/auth/signin/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json())
   }

export default function Login({ setToken }) {
    const history = useHistory();

    const [username, setUserName] = useState();
    const [password, setPassword] = useState();

    const handleSubmit = async e => {
        e.preventDefault();
        const token = await loginUser({
          username,
          password
        });
        setToken(token);
        history.push("/dashboard");
        window.location.reload(false);
      }

    return(
        <div className="login-wrapper">
            <h1>Sign In</h1>
            <form className="login-wrapper" onSubmit={handleSubmit}>
                <label>
                    <p>Username</p>
                    <input type="text" onChange={e => setUserName(e.target.value)} />
                </label>
                <label>
                    <p>Password</p>
                    <input type="password" onChange={e => setPassword(e.target.value)} />
                </label>
                <div>
                    <button type="submit" className="btn btn-primary" >Submit</button>
                </div>
                <a href="/signup">Sign Up</a>
            </form>
        </div>
    )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
  }