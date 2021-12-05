import React, {Component, useState} from 'react';
import { Navigate, useLocation } from 'react-router';


export class LoadScreen extends Component{

    constructor(props) {
        super(props);
        
        let search= window.location.search.substring(9)
        this.state = {queryId: search, redirect: false};
        
        this.handleLoad = this.handleLoad.bind(this);
        this.runQuery = this.runQuery.bind(this);
    }

    componentDidMount() {
    
        window.addEventListener('load', this.handleLoad);
        this.runQuery()
    }

    componentWillUnmount() {
        window.removeEventListener('load', this.handleLoad);
    }
    
    
    runQuery(){
        const {queryId} = this.state
        fetch('http://localhost:8000/run/', {
            method:'POST',
            headers:{
                'Accept':'application/json',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                queryId:queryId
            })
        })
        .then(response=>response.json())
        .then((result)=>{

            if(result['redirect'] == true){

                this.state.redirect = true
                this.setState([this.state.redirect])
            }
        })
        }

    handleLoad(){
        
    }
    render(){
        if(this.state.redirect){
            return(
                <Navigate to='/post/'></Navigate>
            )
        }
        return(
            <div>
                <label>Loading your results. Page will redirect upon completion.</label>
                {this.runQuery}
            </div>
            
        )
        }
    }