var Data = React.createClass({
  render: function() {

    if(this.props['hosts']){
      datalist = this.props.hosts.map(function(host){
        return (
          <li> {host} </li>
        );
      });
    }

    if(this.props['award']){
      console.log(this.props.award);
      console.log(this.props.winner);
      datalist = <li>{this.props.winner}</li>
    }

    return (
      <div className="data">
        <h2 className="dataaward">
          {this.props.award}
        </h2>
        <ol>
        	{datalist}
        </ol>
      </div>
    );
  }
});

var DataList = React.createClass({
  render: function() {
  	var data_nodes = this.props.data.map(function(data){
      if(data['award']){
        return (
          <Data award={data.award} winner={data.winner}>
            {data.winner}
         </Data>
       );
      }
      else if (data['hosts']){
        return (
        <Data hosts={data.hosts}>
          {data.hosts}
        </Data>
        );
      }

  		return (
  			<Data hosts={data.hosts} award={data.award} winner={data.winner}>
          {data.hosts}
          {data.award}
  				{data.winner}
          }
        }
  			</Data>
  		);
  	});
    return (
      <div className="DataList">
        {data_nodes}
      </div>
    );
  }
});

var DataBox = React.createClass({
  load_data: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    this.load_data();
    setInterval(this.load_data, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="DataBox">
        <h1>Hosts</h1>
        <DataList data={this.state.data} />
      </div>
    );
  }
});

React.render(
  <DataBox url="thedata.json" pollInterval={2000} />,
  document.getElementById('content')
);