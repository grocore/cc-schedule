USE [oktell_settings]
GO

/****** Object:  Table [dbo].[A_Users]    Script Date: 7/8/2021 8:25:09 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[A_Users](
	[ID] [uniqueidentifier] NOT NULL,
	[Type] [int] NULL,
	[Name] [nvarchar](200) NULL,
	[FullName] [nvarchar](200) NULL,
	[Priority] [int] NULL,
	[Login] [nvarchar](50) NULL,
	[Password] [nvarchar](50) NULL,
	[Enabled] [bit] NULL,
	[ParentGroupID] [uniqueidentifier] NOT NULL,
	[Info] [nvarchar](1000) NULL,
	[IsDeleted] [bit] NULL,
	[DeleteDT] [datetime] NULL,
 CONSTRAINT [PK_A_Users] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[A_Users] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO

