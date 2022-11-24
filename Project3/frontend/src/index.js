import React from 'react';
import ReactDOM from 'react-dom/client';
import reportWebVitals from './reportWebVitals';
import {Form} from "react-bootstrap";
import Button from 'react-bootstrap/Button';


class Index extends React.Component{
    constructor() {
        super();
        this.state={
            text:'',
            output:[]
        }
        this.handleSubmit=this.handleSubmit.bind(this)
        this.handleChange=this.handleChange.bind(this)
    }
    handleSubmit(e){
        e.preventDefault()
        console.log('asd')
        // var url='http://localhost:5000/?text='
        var url='https://nlpproject.boxz.dev/api?text='
        fetch(url+ this.state.text).then(res=>
            res.json()
        ).then(data=>{
            console.log(data)
            var res=[]
            for (var i=0; i<data.length;i++){
                console.log(data[i])
                if (data[i][1]=='O'){
                    res.push(
                        <span style={{
                            background:'#FFB2A6',
                            color:'#fff',
                            paddingLeft:'5px',
                            paddingRight:'5px',
                            fontSize:'20px',
                            // lineHeight:'30px',
                            borderRadius:'5px'}
                        }>{data[i][0]}</span>
                    )
                }
                else {
                    res.push(
                        <span style={{
                            background:'#56BBF1',
                            color:'#fff',
                            paddingLeft:'5px',
                            paddingRight:'5px',
                            fontSize:'20px',
                            // lineHeight:'30px',
                            borderRadius:'5px'}
                        }>{data[i][0]}</span>
                    )
                }
                res.push(<span>&nbsp; </span>)
            }
            this.setState({
                output:res
            })
        })


    }
    handleChange=e=>{
        this.setState({
            text:e.target.value
        })
        console.log(e.target.value)
    }
    render() {
        return (
            <div style={
                {
                    minHeight:'300px',
                    minWidth:'300px',
                    width:'50vw',
                    // height:'30vh',
                    margin:'auto',
                    position:'relative',
                    top:'50%',
                    transform:'translateY(-50%)',
                    background:'#fff',
                    padding:'20px',
                    borderRadius:'20px'
                }
            }>
                <h1 style={{
                    fontSize:'24px',
                    lineHeight:'35px',
                    textAlign:'center',
                }}>Person Name Recognition</h1>
                <h4 style={{
                    fontSize:'22px',
                    lineHeight:'35px'
                }}>Hi everyone👋. This is the <a href="https://www.cis.um.edu.mo/bsccourses.php?code=CISC3025&year=16" style={{
                    textDecoration: 'none',
                    background:'#FFB2A6',
                    color:'#fff',
                    paddingLeft:'5px',
                    paddingRight:'5px',
                    // fontSize:'20px',
                    // lineHeight:'30px',
                    borderRadius:'5px'
                }}>CISC3025</a> Course Project built by <a href="https://github.com/Super-box" style={{
                    textDecoration: 'none',
                    background:'#56BBF1',
                    color:'#fff',
                    paddingLeft:'5px',
                    paddingRight:'5px',
                    // fontSize:'20px',
                    // lineHeight:'30px',
                    borderRadius:'5px'
                }}>Li Jialin</a> and <a
                    href="https://boxz.dev" style={{
                    textDecoration: 'none',
                    background:'#56BBF1',
                    color:'#fff',
                    paddingLeft:'5px',
                    paddingRight:'5px',
                    // fontSize:'20px',
                    // lineHeight:'30px',
                    borderRadius:'5px'
                }} >Zhang Huakang</a></h4>
                  <Form onSubmit={this.handleSubmit} style={{
                  marginBottom:'2vh'}
                  }>
                      <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Control as="textarea" onChange={this.handleChange} style={{
                            borderColor:'#56BBF1',
                            borderWidth:'3px'
                        }}/>
                      </Form.Group>
                      <Button color={'#FFDDEE'} type="submit" size='lg' style={{
                          width:'100%'
                      }}>
                          Submit
                      </Button>
                  </Form>
                {this.state.output}
                <div style={{marginTop:'2vh'}}><span >Built with <a href="https://reactjs.org/" style={{
                    textDecoration: 'none',
                    background:'#FFB2A6',
                    color:'#fff',
                    paddingLeft:'5px',
                    paddingRight:'5px',
                    // fontSize:'20px',
                    // lineHeight:'30px',
                    borderRadius:'5px'
                }}>React</a> and <a href="https://getbootstrap.com/" style={{
                    textDecoration: 'none',
                    background:'#FFB2A6',
                    color:'#fff',
                    paddingLeft:'5px',
                    paddingRight:'5px',
                    // fontSize:'20px',
                    // lineHeight:'30px',
                    borderRadius:'5px'
                }}>Bootstrap</a>. Source Code on <a href="https://github.com/BoxMars/NLP_Project/tree/master/Project3" style={{
                    textDecoration: 'none',
                    background:'#FFB2A6',
                    color:'#fff',
                    paddingLeft:'5px',
                    paddingRight:'5px',
                    // fontSize:'20px',
                    // lineHeight:'30px',
                    borderRadius:'5px'
                }}>Github</a></span></div>

            </div>
        )
    }
}



const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <div style={{
      background:'#035397',
      height:'100vh',
      width:'100vw'
  }}>

      <Index></Index>
  </div>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
