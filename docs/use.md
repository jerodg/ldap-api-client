# Usage

## ActiveDirectoryApi

Main ActiveDirectoryApi API class, containing the following methods.

### \_\_init\_\_

Initialize the ActiveDirectoryApi API.

Pre-configured method.

### \_\_enter\_\_

Built-in method; requires no configuration.

### \_\_exit\_\_

Built-in method; requires no configuration.

### *async* get_users --> dict

Query Actve Directory for users.

#### Returns

<pre>

	<b>dict</b>
	
	Dict of users on Active Directory.
	
</pre>

### *async* get_computers --> dict

Query Actve Directory for computers.

#### Returns

<pre>

	<b>dict</b>
	
	Dict of computers on Active Directory.
	
</pre>

### *@dataclass* User

Contains information regarding a user on AD.

#### Attributes

<pre>

	<b>ident</b> : str
	
	User/Employee ID.
	
</pre>


<pre>

	<b>name</b> : str
	
	User/Employee name.
	
	default = None
	
</pre>


<pre>

	<b>memberof</b> : Any
	
	Rule groupes that to which a user/employee belongs.
	
	default = None
	
</pre>


<pre>

	<b>department</b> : Any
	
	User/Employee department.
	
	default = None
	
</pre>


<pre>

	<b>manager</b> : str
	
	User/Employee manager.
	
	default = None
	
</pre>


<pre>

	<b>title</b> : Any
	
	User/Employee title.
	
	default = None
	
</pre>

*Note:* User attributes are processed after init to be semi-colon (;) separated.

### *@dataclass* Computer

Contains information regarding a computer on AD.

#### Attributes

<pre>

	<b>name</b> : str
	
	Computer name.
	
</pre>

<pre>

	<b>last_logon</b> : str
	
	Datetime of last logon.
	
</pre>




