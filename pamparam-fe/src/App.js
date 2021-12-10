import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react';

class App extends React.Component {

  render(){
    return (
      <div className="App">
        <header className="App-header">
          <Clock />
          <img src={logo} className="App-logo" alt="logo" />
        </header>
        <TickerList/>
      </div>
    );
  }
}

class TickerList extends React.Component{
  constructor(props){
    super(props);
    this.state = {value:'nothing', selection:'nothing' ,list: {'nothing':"...","1min":"1 Minute","15min":"15 Minutes","1hr":"1 Hours","4hr":"4 Hours","1d":"1 Day"}};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);     
  }

  handleChange(event) {    
    this.setState({value: event.target.value});
    //this.setState({selection: 'nothing'});
    }

  handleSubmit(event){
    this.setState({selection: 'nothing'})
    this.setState({selection: this.state.value});
    event.preventDefault();
  }
  render(){
    if(this.state.selection !== 'nothing'){
      return(
        <div>
        <form onSubmit={this.handleSubmit}>
          <label style={{color: "white"}}>
          Select an interval:
          <select className="form-select form-select-lg" onChange={this.handleChange}>
            {Object.keys(this.state.list).map((d,key) => {
              return <option key={key} value = {d}> {this.state.list[d]} </option>;
            })}
          </select>    
          </label>
          <br></br>
          <br></br>
          <input className="btn btn-primary" type="submit" value="Submit" />
        </form>
        <br></br>
        <p style={{color: "white"}}>Currently Displaying:{this.state.selection}</p>
        <ApiCall selection={this.state.selection} />
        </div>
      );
  }
    
    return(<div>
        <form onSubmit={this.handleSubmit}>
          <label style={{ color: "white"}}>
          Select an interval:
          <select className="form-select form-select-lg" onChange={this.handleChange}>
            {Object.keys(this.state.list).map((d,key) => {
              return <option key={key}value = {d}> {this.state.list[d]} </option>;
            })}
          </select> 
          </label>
          <br></br>
          <br></br>
          <input className="btn btn-primary" type="submit" value="Submit" />
        </form>
        <br></br>
        </div>
      );
  }
}


class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {date: new Date()};
  }
  componentDidMount() {
    this.timerID = setInterval(
      () => this.tick(),
      1000
      );
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }
  tick() {
    this.setState({date: new Date()});
  }

  render() {
    return(
        <h>{this.state.date.toLocaleTimeString()}</h>
      );
  }
}
function ApiCall(props) {
    const [apiData, setApiData] = useState({"loading":{"loading1":"loading","loading2":"loading","signal":"loading"}});
    useEffect(() => {
      setApiData({"loading":{"loading1":"loading","loading2":"loading","signal":"loading"}});
      fetch(props.selection).then(res => res.json()).then(data => {setApiData(data);
      });
    },[props.selection]);


    return(
      <div>
      <table className="table table-dark">
        <thead>
          <tr>
          <th scope = "col">Exchange</th>
          <th scope = "col">%d</th>
          <th scope = "col">%k</th>
          <th scope = "col">Signal</th>
          </tr>
          {Object.keys(apiData).map((d,key) => {
            return(<tr>
            <th key = {key}> {d}</th>
            <ListElement key={key} obj = {apiData[d]}/>
            </tr>);
          })
        }
        </thead>
        <tbody>
        </tbody>
      </table>
      </div>
      );
  }
  function ListElement(props) {
    const obj = props.obj;
    const kk = props.key*100+111;
    return Object.keys(obj).map((d,key) =>
    <th key = {kk}>
      {obj[d]}
    </th>
    );
    
  }



export default App;
