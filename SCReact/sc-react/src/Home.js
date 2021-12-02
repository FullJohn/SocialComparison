import React, {Component, useState} from 'react';
import { Tab } from 'react-bootstrap';
import DatePicker from 'react-date-picker';

export class Home extends Component{

    constructor(props) {
        super(props);
        
        this.state = {platform: 'YouTube', brand1: '', brand2: '', brand3: '', startDate: new Date(), endDate: new Date()};
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.startDateChange = this.startDateChange.bind(this);
        this.endDateChange = this.endDateChange.bind(this);
      }
      

      startDateChange(date) {this.setState({startDate:date}); }
      endDateChange(date) {this.setState({endDate: date}); }
      handleChange(event) {this.setState({[event.target.name]: event.target.value}); }
      handleSubmit(event) {
  
        const { platform, brand1, brand2, brand3, startDate, endDate} = this.state
        event.preventDefault();
        alert('Selected platform: ' + this.state.platform + '\nBrand 1: ' + this.state.brand1 + '\nBrand 2: ' + this.state.brand2
        + '\nBrand 3: ' + this.state.brand3 + '\nStart Date: ' + this.state.startDate + '\nEnd Date: ' + this.state.endDate);
      }


    render(){
        return(
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
            <input type="submit" value="Submit" />
            
          </form>
        );
    }
}