import React, { useState, useEffect } from 'react';
import { useHistory } from "react-router-dom";

export default function Dashboard( token ) {
    const history = useHistory();

    const [ notes, setNotes ] = useState([]);
    const [ title, setTitle ] = useState("");
    const [ description, setDescription ] = useState("");
    const [ updatingNoteId, setUpdatingNoteId ] = useState(0);
    const [ updatingNoteTitle, setUpdatingNoteTitle ] = useState("");
    const [ updatingNoteDescription, setUpdatingNoteDescription ] = useState("");

    async function fetchNotes() {
        return fetch('http://localhost:8000/api/v1/note/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token?.token.token
          }
        })
          .then(data => data.json())
          .then(notes => {setNotes(notes)})
       }

    async function createNote() {
        return fetch('http://localhost:8000/api/v1/note/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token?.token.token
          },
          body: JSON.stringify({title: title, description: description})
        })
          .then(data => data.json())
          .then(note => {
            setNotes(notes.concat(note)); 
            setTitle(""); 
            setDescription("");
        })
       }

    async function updateNote() {
        return fetch('http://localhost:8000/api/v1/note/' + updatingNoteId + '/', {
            method: 'PUT',
            headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token?.token.token
            },
            body: JSON.stringify({title: updatingNoteTitle, description: updatingNoteDescription})
        })
            .then(data => data.json())
            .then(() => fetchNotes())
    }

    async function deleteNote(noteId) {
        return fetch('http://localhost:8000/api/v1/note/' + noteId + '/', {
            method: 'DELETE',
            headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token?.token.token
            }
        })
            .then(data => data.json())
            .then(setNotes(notes.filter((i) => i.id !== parseInt(noteId))))
    }

    useEffect(() => {
        fetchNotes()
	}, []);

    return (
        <div className="container">
          <div classname="jumbotron">
            <h1 className="display-4">Notes App</h1>
            <p>Your are authorized as <b>{token.token.username}</b></p>
            <button type="button" className="btn btn-primary" onClick={() => {localStorage.clear(); history.push("/signin"); window.location.reload(false);}}>Logout</button>
          </div>
          {notes && notes.map((note) => (
            <div className="card" key={note.id}>
                <div className="card-header">
                    {
                    note.id == updatingNoteId
                    ? <input placeholder='Title' value={updatingNoteTitle} onChange={e => setUpdatingNoteTitle(e.target.value)} />
                    : <p><b>{note.title}</b> ({ new Date(note.created_at).toLocaleString()})</p>
                    }
                </div>
                <div className="card-body">
                    {
                        note.id == updatingNoteId
                        ? <input placeholder='Description' value={updatingNoteDescription} onChange={e => setUpdatingNoteDescription(e.target.value)} />
                        : <p className="card-text">{note.description}</p>
                    }
                </div>
                <button type="button" className="btn btn-primary" id={note.id} onClick={
                    (e) => {
                        if (note.id != updatingNoteId) { 
                            setUpdatingNoteId(e.target.id); 
                            setUpdatingNoteTitle(note.title); 
                            setUpdatingNoteDescription(note.description);
                        }
                        else {
                            updateNote();
                            setUpdatingNoteId(0);
                        }
                    }
                }>
                    {note.id != updatingNoteId ? "Edit" : "Save"}
                </button>
                <button type="button" className="btn btn-danger" id={note.id} onClick={(e) => deleteNote(e.target.id)}>Delete</button>
            </div>
          ))}
          <div className="card">
              <div className="card-header">
                <input placeholder='Title' value={title} onChange={e => setTitle(e.target.value)} />
              </div>
              <div className="card-body">
                <input placeholder='Description' value={description} onChange={e => setDescription(e.target.value)} />
              </div>
              <button type="button" className="btn btn-primary" onClick={() => createNote()}>Create</button>
            </div>
        </div>
      );
}