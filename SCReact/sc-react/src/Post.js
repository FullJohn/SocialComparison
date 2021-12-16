import React, {Component} from 'react';
import {Table} from 'react-bootstrap';

export class Post extends Component{
    
    constructor(props){
        super(props);
        let search= window.location.search.substring(9)
        this.state={queryId: search, posts:[]}
    }

    refreshList(){
        const { queryId } = this.state
        fetch('http://54.144.107.206:8000/post/', {
            method:'POST',
            headers:{
                'Accept':'application/json',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                getPosts:true,
                queryId:queryId
            })
        })
        .then(response=>response.json())
        .then(data=>{
            this.setState({posts:data});
        });
    }

    componentDidMount(){
        this.refreshList();
    }

    componentDidUpdate(){
        this.refreshList();
    }

    render(){
        const {posts} = this.state;
        return(
            <div>
                <Table className="mt-4" striped bordered hover size="sm">
                    <thead>
                        <tr>
                            <th>PostId</th>
                            <th>url</th>
                            <th>title</th>
                            <th>description</th>
                            <th>thumbnail</th>
                            <th>channel</th>
                            <th>date</th>
                            <th>views</th>
                            <th>comments</th>
                            <th>likes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {posts.map(post=>
                            <tr key={post.PostId}>
                                <td>{post.PostId}</td>
                                <td>{post.url}</td>
                                <td>{post.title}</td>
                                <td>{post.description}</td>
                                <td>{post.thumbnail}</td>
                                <td>{post.channel}</td>
                                <td>{post.date}</td>
                                <td>{post.views}</td>
                                <td>{post.comments}</td>
                                <td>{post.likes}</td>
                            </tr>)}
                    </tbody>
                </Table>
            </div>
        )
    }
}