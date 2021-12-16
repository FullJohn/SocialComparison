import Button from '@restart/ui/esm/Button';
import React, {Component, useEffect, useState} from 'react';
import { Tab } from 'react-bootstrap';
import DatePicker from 'react-date-picker';
import { Navigate } from 'react-router';








export class Home extends Component{

    constructor(props) {
        super(props);

        this.state = {queryId: '', platform: 'YouTube', brand1: '', brand2: '', brand3: '', startDate: new Date(), endDate: new Date(), redirect: false, queryId: ''};
  
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.startDateChange = this.startDateChange.bind(this);
        this.endDateChange = this.endDateChange.bind(this);
    
      }
      
      startDateChange(date) {this.setState({startDate:date}); }
      endDateChange(date) {this.setState({endDate: date}); }
      handleChange(event) {this.setState({[event.target.name]: event.target.value}); }
      handleSubmit(event) {
        const { platform, brand1, brand2, brand3, startDate, endDate} = this.state;
    

        
        event.preventDefault();
        fetch('http://54.144.107.206:8000/query/', {
            method:'POST',
            headers:{
                'Accept':'application/json',
                'Content-Type':'application/json',
            },
            body:JSON.stringify({
                platform:platform,
                brand1:brand1,
                brand2:brand2,
                brand3:brand3,
                startDate:startDate,
                endDate:endDate
            })
        })
        .then(response=>response.json())

        .then((result)=>{
            
        
            if(result['redirect'] == true){
                
                this.state.queryId = result['queryId']
                this.setState([this.state.queryId])
                
                this.state.redirect = true
                this.setState([this.state.redirect])
            }
            
            else{
                alert(result['message']);
            }
        
        })
    }


    render(){
        if(this.state.redirect){
            const url = "/loading?queryId=" + this.state.queryId
            return(
            <Navigate to={url}></Navigate>)
        }
        return(
            <div>
                <form onSubmit={this.handleSubmit}>
                    <label htmlFor='platform'>Select a platform:</label>
                        <select name='platform' placeholder = 'YouTube' value={this.state.platform} onChange={this.handleChange}>
                            <option value="youtube">YouTube</option>
                            <option value="facebook">Facebook</option>
                            <option value="instagram">Instagram</option>
                            <option value="twitter">Twitter</option>
                            <option value="pinterest">Pinterest</option>
                            <option value="tiktok">TikTok</option>
                        </select>
                    <br></br>
                    <label htmlFor="startDate">Start Date:</label>
                        <DatePicker type="date" name="startDate" value={this.state.startDate}
                        onChange={this.startDateChange} required={true} dayPlaceholder="dd" monthPlaceholder="mm" yearPlaceholder="yyyy"
                        clearIcon={null}></DatePicker>
                    <t></t>
                    <label htmlFor="endDate">End Date:</label>
                        <DatePicker type="date" name="endDate" value={this.state.endDate}
                        onChange={this.endDateChange} required={true} dayPlaceholder="dd" monthPlaceholder="mm" yearPlaceholder="yyyy"
                        clearIcon={null}></DatePicker>
                    
                    <br></br>
                    
                    <label htmlFor='brand1'>Brand 1:</label>
                        <input type="text" name="brand1" value={this.state.brand1} onChange={this.handleChange}/>
                    <label htmlFor='brand2'>Brand 2:</label>
                        <input type="text" name="brand2" value={this.state.brand2} onChange={this.handleChange}/>
                    <label htmlFor='brand3'>Brand 3:</label>
                        <input type="text" name="brand3" value={this.state.brand3} onChange={this.handleChange}/>
                    <br></br>

                    <input type='submit' value='Submit'></input>
                    </form>
                    
                </div>
            );
    }
}
