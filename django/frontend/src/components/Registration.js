import React, { useState } from 'react';
import './Login.css';
import PropTypes from 'prop-types';
import { useHistory } from "react-router-dom";

async function registerUser(credentials) {
    return fetch('http://localhost:8000/api/v1/auth/signup/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json())
   }

export default function Registration({ setToken }) {
    const history = useHistory();

    const [username, setUserName] = useState();
    const [password, setPassword] = useState();

    const handleSubmit = async e => {
        e.preventDefault();
        const token = await registerUser({
          username,
          password
        });
        setToken(token);
        history.push("/dashboard");
        window.location.reload(false);
      }

    return(
        <div className="login-wrapper">
            <h1>Sign Up</h1>
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
                <a href="/signin">Sign In</a>
            </form>
        </div>
    )
}

Registration.propTypes = {
    setToken: PropTypes.func.isRequired
  }