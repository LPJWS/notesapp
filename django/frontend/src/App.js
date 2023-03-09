import React from 'react';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import Registration from './components/Registration';
import useToken from './components/useToken';
import './App.css';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

const base_url = "http://localhost:8000/api/v1/"

function App() {
  const { token, setToken } = useToken();
  if(!token && !(["/signin", "/signup"].includes(window.location.pathname))) {
    return <Login setToken={setToken} />
  }

  return (
      <div className="wrapper">
        <BrowserRouter>
          <Switch>
            <Route exact path="/">
              <Dashboard token={token}/>
            </Route>
            <Route path="/dashboard">
              <Dashboard token={token}/>
            </Route>
            <Route path="/signin">
              <Login setToken={setToken}/>
            </Route>
            <Route path="/signup">
              <Registration setToken={setToken}/>
            </Route>
          </Switch>
        </BrowserRouter>
      </div>
  );
}

// class App extends Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       notes: []
//     }
//   }

//   componentDidMount() {
//     const url = base_url + "note/";
//     // localStorage.setItem("token", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZXhwaXJlIjoiMjAyMy0wNC0wNiAxMjoxMjoyNC40MDMyOTEifQ.JKryDRk7w0SL5kaxz86ej-Jtl-e24VjQXIHkdxDpZgc")
//     var token = localStorage.getItem('token');
//     console.log(token);
//     fetch(url, {headers: {"Authorization": "Bearer " + token}})
//     .then(response => response.json())
//     .then(json => this.setState({ notes: json }))
//   }

export default App;