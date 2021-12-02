import React, {Component, useState} from 'react';


export class LoadScreen extends Component{

    constructor(props) {
        super(props);
    
        this.state = {queryId: this.props.queryId,toPostResults: false};
        this.runQuery = this.runQuery.bind(this);
    }

    runQuery(){
        fetch(process.env.REACT_APP_API + 'run/', {
            method:'POST',
            headers:{
                'Accept':'application/json',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                queryId:this.props.queryId
            })
        })
        .then(response=>response.json())
        .then((result)=>{
            this.setState({[this.state.toPostResults]:result['redirect']}); 
        })
        }

        render(){
            return(
                <label>Testing</label>
            )
        }
    }
    
